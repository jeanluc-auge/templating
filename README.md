# FLASK code generated with jinja templating

- automates the creation of Flask endpoints
- code is gnerated with jinja templating

**This is the full version with code inspection**

With the following modules: 
- The macros functions are implemented in *macros.py*
- The definition of endpoints and macros to expose in *cep.py*
- jinja template of a Flask endpoint in *template_endpoints*
- The code inspection to build the data model and fill the jinja tempalte in *generate_endpoints.py*

Automates the creation of Flask endpoints in a dynamic way with meta programming:
- build data model with code inspection
- code templating with jinja2 

## use
pip3 install -rrequirements.txt <br>

**Code templating**:<br>
python3 generate_endpoints.py<br>
=> copy/paste the generated code output in flask_restplus_server.py<br>

**Launch the Flask server**:<br>
python3 flask_restplus_server.py

You can add or remove macros to expose in cep.py
