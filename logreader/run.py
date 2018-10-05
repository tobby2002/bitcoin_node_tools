# When creating packages, the import app below gets from
# __init__.py file`

from logreader import app

if __name__ == '__main__':
    app.run(debug=True)
