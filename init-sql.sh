echo "Initiating"
flask db init

echo "migrating"
flask db migrate

echo "upgrading"
flask db upgrade