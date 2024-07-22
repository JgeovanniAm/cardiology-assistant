
## Run Locally

Clone the project

```bash
  git clone https://github.com/JgeovanniAm/cardiology-assistant
```

Go to the project directory

```bash
  cd cardiology-assistant
```

Setup pip

```bash
  python3 -m venv .venv  
```
```bash
  source .venv/bin/activate
```

Install dependencies

```bash
  pip install -r lib.txt      
```

Start the server

```bash
  flask --app app run
```
or

```bash
  flask run --cert=adhoc
```
