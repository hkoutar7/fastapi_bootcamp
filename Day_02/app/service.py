from fastapi import HTTPException, status
from app.data import close_database_connection, database_connection
from app.schema import ProductSchema, CreateProductSchema, UpdateProductSchema

def retrieve_products() -> list :
    connection = database_connection()
    
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM PRODUCTS")
    columns = [col.name for col in cursor.description] 
    products = [dict(zip(columns, row)) for row in cursor.fetchall()]
    cursor.close()

    close_database_connection(connection)

    return products


def retrieve_product(id : str) -> tuple | None:
    connection = database_connection()
    
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM PRODUCTS where id = %s""",(str(id),))
    product = cursor.fetchone()
    cursor.close()

    close_database_connection(connection)

    if not product :
        return None

    product_dict = {}
    product_dict["id"] = product[0]
    product_dict["title"] = product[1]
    product_dict["content"] = product[2]
    product_dict["is_published"] = product[3]
    product_dict["created_at"] = product[4]

    return product_dict


def add_product(payload : CreateProductSchema) -> None | dict :
    connection = database_connection()
    
    cursor = connection.cursor()
    cursor.execute("""INSERT INTO products(title, content) values (%s, %s) returning *""", (payload.title, payload.content))
    connection.commit()
    product = cursor.fetchone()
    cursor.close()

    product_dict = {}
    product_dict["id"] = product[0]
    product_dict["title"] = product[1]
    product_dict["content"] = product[2]
    product_dict["is_published"] = product[3]
    product_dict["created_at"] = product[4]

    close_database_connection(connection)

    return product_dict


def update_product_by_id(id : int , payload : UpdateProductSchema) -> dict | None:
    connection = database_connection()
    
    cursor = connection.cursor()
    cursor.execute("""UPDATE products SET title=%s, content=%s ,is_published=%s where id = %s returning *""",
                (payload.title, payload.content, payload.is_published, str(id)))
    connection.commit()
    product = cursor.fetchone()
    cursor.close()
    close_database_connection(connection)

    if not product :
        return None

    product_dict = {}
    product_dict["id"] = product[0]
    product_dict["title"] = product[1]
    product_dict["content"] = product[2]
    product_dict["is_published"] = product[3]
    product_dict["created_at"] = product[4]

    return product_dict


def delete_product_by_id(id : int) -> dict | None :
    connection = database_connection()
    
    cursor = connection.cursor()
    cursor.execute("""DELETE FROM products WHERE id=%s returning *""", (str(id),))
    connection.commit()
    product = cursor.fetchone()
    cursor.close()

    close_database_connection(connection)

    if not product :
        return None
    
    product_dict = {}
    product_dict["id"] = product[0]
    product_dict["title"] = product[1]
    product_dict["content"] = product[2]
    product_dict["is_published"] = product[3]
    product_dict["created_at"] = product[4]

    return product_dict

