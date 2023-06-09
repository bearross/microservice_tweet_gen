import base64
from client import client, info
import asyncio


async def test_archive_upload():
    client.headers = {
        "Authorization": "Token " + info["token"]
    }

    file_header = "data:application/zip;base64,"
    with open("files/Archive-trimmed.zip", 'rb') as archive:
        query = """
                mutation uploadArchive($archive: Upload) {
                    uploadArchive(archive:$archive) {
                        archiveId,
                        accountId,
                        archive,
                        statusUrl,
                        errors{
                            key,
                            messages
                        }
                    }
                }
            """
        archive = archive.read()
        archive = file_header + base64.b64encode(archive).decode("UTF-8")
        variables = {"archive": archive}
        data = client.execute(query=query, variables=variables)
        print(data)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(test_archive_upload())
