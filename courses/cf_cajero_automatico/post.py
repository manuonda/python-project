from abc import ABC,abstractmethod

class Post():
    def __init__(self, id, title, content):
        self.id = id
        self.title = title
        self.content = content

from typing import TypeVar, Generic, Dict, List

# Definir el tipo genérico T
T = TypeVar('T')

class Repository (Generic[T], ABC):

    @abstractmethod
    def get(self, id)-> T:
        raise NotImplementedError
    
    @abstractmethod
    def get_all(self) -> list[T]:
        raise NotImplementedError
    
    @abstractmethod
    def add(self, value)->None:
        raise NotImplementedError

    @abstractmethod
    def update(self, id, value) ->None:
        raise NotImplementedError
     
    @abstractmethod
    def delete(self, id)->None:
        raise NotImplementedError
    

class PostRepository(Repository[Post]):
    def __init__(self,posts:dict[int, Post] = None):
        self.posts = posts if posts is not None else {}

    def get(self, id) -> Post:
        return self.posts[id]
    
    def get_all(self) ->list[Post]:
        return list(self.posts.values())
    
    def add(self, entry) ->None:
        self.posts[entry.id] = entry

    def update(self, entry) -> None:
        if entry.id is None:
            raise ValueError("No se puede actualizar el post")
        self.posts[entry.id] = entry

    def delete(self, entry) -> None:
        if entry.id is None:
            raise ValueError("No se puede eliminar el post")
        del self.posts[entry.id]