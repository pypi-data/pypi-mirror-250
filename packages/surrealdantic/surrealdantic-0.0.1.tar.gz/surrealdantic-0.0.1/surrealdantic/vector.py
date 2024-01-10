from __future__ import annotations

from datetime import datetime
from typing import (Any, AsyncGenerator, Optional, ParamSpec, TypeAlias,
                    TypedDict, TypeVar, Union)

import numpy as np
from pydantic import computed_field, root_validator
from surrealdb import Surreal

from surrealdantic import Model

T = TypeVar("T", bound=np.ndarray)  # type: ignore
P = ParamSpec("P")
Value: TypeAlias = Union[int, float, str, bool, list[str]]
MetaData: TypeAlias = Optional[dict[str, Value]]
A = TypeVar("A", bound=Any, covariant=True)


class SearchEmbedding(TypedDict):
	"""
	Represents an embedding used for search.

	Attributes:
		score (float): The score of the embedding.
		id (str): The ID of the embedding.
		metadata (MetaData): The metadata associated with the embedding.
	"""
	score: float
	id: str
	metadata:MetaData


def cosine_similarity(
	*, this: np.ndarray[float, A], that: np.ndarray[float, A]
) -> float:
	"""
	Computes the cosine similarity between two vectors.
	The vectors must have the same shape, otherwise a ValueError is raised.
	This function can be optimized by using a JIT compiler like Numba or running it on GPU.

	Arguments:

	self -- The first vector.
	other -- The second vector.
	"""
	raw = this @ that.T / (np.linalg.norm(this) * np.linalg.norm(that, axis=0))
	return np.round(raw, 7) if raw > 0 else 0  # type: ignore


class Embedding(Model):
	values: np.ndarray[float, Any] | list[float]
	metadata: MetaData

	@computed_field
	def dimensionality(self) -> int:
		return np.shape(self.values)[0]

	@computed_field
	def updated_at(self) -> datetime:
		return datetime.now()

	async def same_dim(self, *, db: Surreal) -> AsyncGenerator[dict[str, Any], None]:
		"""
		Find all embeddings in the database that have the same dimensionality as this one.
		"""
		response = await db.query(
			f"""
			SELECT id
			FROM {self.__class__.__name__}
			WHERE dimensionality = {self.dimensionality}
			"""
		)
		for row in response:
			yield row

	async def create(self, *, db: Surreal):
		"""
		Create a new record in the database.

		Parameters:
		- db: The database connection object.

		Returns:
		None
		"""
		await db.create(
			self.__class__.__name__,
			{
				**self.dict(),
				"values": self.values.tolist(),
				"updated_at": datetime.now().isoformat(),
			},
		)

	async def stream(self, *, db: Surreal):
		"""
		Streams search results from the database based on the query_same_dim method.

		Args:
			db (Surreal): The database connection object.

		Yields:
			SearchEmbedding: A search embedding object containing the score, id, and metadata.
		"""
		async for i in self.same_dim(db=db):
			prev: float = 0.0
			response = await db.query(
				"SELECT values, metadata " +
				f"FROM {self.__class__.__name__} " +  # type: ignore
				f"WHERE id = {i['result'][0]['id']};"  # type: ignore
			)  # type: ignore
			result = response[0]["result"][0]
			vector = np.array(result["values"])
			new = cosine_similarity(this=self.values, that=vector)
			if new > prev:
				prev = new
				yield SearchEmbedding(
					score=new,
					id=result["id"],
					metadata=result["metadata"],
				)
			vector = np.array(result["values"])
			new = cosine_similarity(this=self.values, that=vector)
			if new > prev:
				prev = new
				yield SearchEmbedding(
					score=new,
					id=result["id"],
					metadata=result["metadata"],
				)
			new = cosine_similarity(this=self.values, that=vector)
			if new > prev:
				prev = new
				yield SearchEmbedding(
					score=new,
					id=result["id"],
					metadata=result["metadata"],
				)
