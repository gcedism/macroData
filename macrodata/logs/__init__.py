from pathlib import Path
FOLDER = str(Path(__file__).parent)

from .logComponents import logHeader

LOGGING_CONFIG = { 
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': { 
        'console': { 
            'format': '[%(levelname)s] %(name)s: %(message)s'
        },
        'file': { 
            'format': '[%(levelname)s] %(name)s: %(message)s'
        }
    },
    'handlers': { 
        'console': { 
            'level': 'WARNING',
            'formatter': 'console',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
        'file_explorer': { 
            'level': 'DEBUG',
            'formatter': 'file',
            'class': 'logging.FileHandler',
            'filename': FOLDER + '/explorer.log',
            'mode' : 'w'
        },
        'file_manager': { 
            'level': 'DEBUG',
            'formatter': 'file',
            'class': 'logging.FileHandler',
            'filename': FOLDER + '/manager.log',
            'mode' : 'w'
        },
        'file_manager_clients': { 
            'level': 'DEBUG',
            'formatter': 'file',
            'class': 'logging.FileHandler',
            'filename': FOLDER + '/clients.log',
            'mode' : 'w'
        },
    },
    'loggers': { 
        '': {  # root logger
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False
        },
        '__main__': {  # if __name__ == '__main__'
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'macrodata.explorer': {  
            'handlers': ['console', 'file_explorer'],
            'level': 'DEBUG',
            'propagate': True
        },
        'macrodata.manager': {  
            'handlers': ['console', 'file_manager'],
            'level': 'DEBUG',
            'propagate': True
        },
        'macrodata.clients': {  
            'handlers': ['console', 'file_manager_clients'],
            'level': 'DEBUG',
            'propagate': True
        }
    } 
}