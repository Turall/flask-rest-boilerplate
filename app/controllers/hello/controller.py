def search(name=None):
    message = "Hello, %s!"
    return {"message": message % name if name else message % "World"}
