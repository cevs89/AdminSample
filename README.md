# Basic Requirements:
`>= Python 3x`

# Virtual environment

### Step 1
`virtualenv <path> --python=python3`

### Step 2
`source <path>/bin/activate`

### Step 3
`pip install -r requeriments.txt`

# To generate the database, the following command is executed:
`python manage.py migrate`

# To generate a new super user admin
`python manage.py createsuperuser`
