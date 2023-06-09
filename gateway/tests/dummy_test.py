

def test_dummy(client):
    query = """
        mutation createPerson($name: String) {
            createPerson(name:$name) {
                person{
                    age,
                    name
                },
                ok
            }
        }
    """
    variables = {"name": "John Doe"}

    data = client.execute(query=query, variables=variables)
    print(data)
