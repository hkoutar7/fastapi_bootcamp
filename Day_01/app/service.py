from random import randint

from app.data import posts as _posts


def retrieve_posts() -> list :
    return _posts


def retrieve_post_by_id(id : int) -> dict | None :
    for p in _posts :
        if p["id"] == id :
            return p
    return None


def add_post(payload) -> None | dict :
    post = {}
    id = randint(0, 100)
    post["id"] = id
    
    if "title" in payload :
        post["title"] = payload["title"]

    if "description" in payload :
        post["description"] = payload["description"]
    
    _posts.append(post)
    return post


def update_post_by_id(id : int, payload) -> dict | None :
    is_exist = retrieve_post_by_id(id)

    if is_exist is None :
        return None
    
    post = is_exist
    if "title" in payload :
        post["title"] = payload["title"]

    if "description" in payload :
        post["description"] = payload["description"]

    return post


def delete_post_by_id(id : int) -> None | dict :
    is_exist = retrieve_post_by_id(id)

    if is_exist is None :
        return None
    
    _posts.remove(is_exist)
    return is_exist


def retrieve_latest_post() -> None | dict :
    lenght = len(_posts)

    if lenght > 0 :
        return _posts[lenght - 1]
    return None


