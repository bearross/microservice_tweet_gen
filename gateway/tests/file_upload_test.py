import unittest
import base64
from client import client


async def test_upload_file():
    file_header = "data:application/zip;base64,"
    with open("files/a.zip", 'rb') as file:
        query = """
                mutation uploadFile($file: Upload) {
                    uploadFile(file:$file) {
                        ok
                    }
                }
            """
        file = file.read()
        file = file_header + base64.b64encode(file).decode("UTF-8")
        variables = {"file": file}
        data = client.execute(query=query, variables=variables)

        return data

