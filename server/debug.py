#!/usr/bin/env python3

from server.main import app
from models import db, Plant

if __name__ == '__main__':
    
    with app.app_context():
        import ipdb; ipdb.set_trace()
