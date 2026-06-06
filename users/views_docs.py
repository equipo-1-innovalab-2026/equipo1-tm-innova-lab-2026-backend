import os
from django.shortcuts import render
from django.conf import settings

def developer_portal(request):
    """
    Vista del Portal de Desarrolladores.
    Lee los archivos de documentación en formato Markdown y los envía a la plantilla
    para ser renderizados dinámicamente con soporte para diagramas de Mermaid.
    """
    base_dir = settings.BASE_DIR
    endpoints_path = os.path.join(base_dir, 'documentacion', 'endpoints_guide.md')
    data_dict_path = os.path.join(base_dir, 'documentacion', 'data_dictionary.md')
    
    endpoints_content = ""
    if os.path.exists(endpoints_path):
        with open(endpoints_path, 'r', encoding='utf-8') as f:
            endpoints_content = f.read()
            
    data_dict_content = ""
    if os.path.exists(data_dict_path):
        with open(data_dict_path, 'r', encoding='utf-8') as f:
            data_dict_content = f.read()
            
    return render(request, 'users/developer_portal.html', {
        'endpoints_markdown': endpoints_content,
        'data_dict_markdown': data_dict_content
    })
