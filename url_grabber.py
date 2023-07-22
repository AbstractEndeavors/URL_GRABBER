import requests
import ssl
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
from urllib3.util import ssl_
import PySimpleGUI as sg
import inspect
import re
from abstract_utilities.class_utils import *
def get_ciphers():
    return "ECDHE-RSA-AES256-GCM-SHA384,ECDHE-ECDSA-AES256-GCM-SHA384,ECDHE-RSA-AES256-SHA384,ECDHE-ECDSA-AES256-SHA384,ECDHE-RSA-AES256-SHA,ECDHE-ECDSA-AES256-SHA,ECDHE-RSA-AES128-GCM-SHA256,ECDHE-RSA-AES128-SHA256,ECDHE-ECDSA-AES128-GCM-SHA256,ECDHE-ECDSA-AES128-SHA256,AES256-SHA,AES128-SHA".split(',')

def get_gui_fun(name: str = '', args: dict = {}):
    import PySimpleGUI
    return get_fun({"instance": PySimpleGUI, "name": name, "args": args})

def expandable(size: tuple = (None, None)):
    return {"size": size, "resizable": True, "scrollable": True, "auto_size_text": True, "expand_x": True, "expand_y": True}

def change_glob(var: any, val: any):
    globals()[var] = val
    return val

def get_parser_choices():
    bs4_module = inspect.getmodule(BeautifulSoup)
    docstring = bs4_module.__builtins__
    start_index = docstring.find("Supported parsers are:")
    end_index = docstring.find(")", start_index)
    choices_text = docstring[start_index:end_index]
    choices = [choice.strip() for choice in choices_text.split(",")]
    return choices

def add_string_list(ls: (list or str), delim: str = '', string: str = ''):
    input(ls)
    if isinstance(ls,str):
        ls = list(ls.split(','))
    if isinstance(ls,list):
        string = ''
        for part in ls:
            string = string+delim+part
    return string
    


def create_ciphers_string(ls: list = get_ciphers()):
    
    cipher_string = add_string_list(ls=ls, delim=':')[:-1]

    globals()['CIPHERS'] = cipher_string
    return cipher_string

create_ciphers_string()

def get_browsers():
    return 'Chrome,Firefox,Safari,Microsoft Edge,Internet Explorer,Opera'.split(',')

def get_user_agents():
    return ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59',
            'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14']

def create_user_agent(user_agent: str = get_user_agents()[0]):
    return {"user-agent": user_agent}

def get_operating_systems():
    return ['Windows NT 10.0', 'Macintosh; Intel Mac OS X 10_15_7', 'Linux', 'Android', 'iOS']

def ssl_options():
    return ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_COMPRESSION

def get_user_agent():
    return {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"}

class TLSAdapter(HTTPAdapter):
    def __init__(self, ssl_options=0, *args, **kwargs):
        self.ssl_options = ssl_options
        super().__init__(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs):
        context = ssl_.create_urllib3_context(ciphers=CIPHERS, cert_reqs=ssl.CERT_REQUIRED, options=self.ssl_options)
        self.poolmanager = PoolManager(*args, ssl_context=context, **kwargs)

def create_columns(ls, i, k):
    if float(i) % float(k) == float(0.00) and i != 0:
        lsN = list(ls[:-k])
        lsN.append(list(ls[-k:]))
        ls = lsN
    return ls

def get_cypher_checks(ciphers: list = get_ciphers()):
    ls = [[[sg.Text('CIPHERS: ')], sg.Multiline(CIPHERS, key='-CIPHERS_OUTPUT-', size=(80, 5), disabled=False)]]
    for k in range(0, len(ciphers)):
        ls.append(sg.Checkbox(ciphers[k], key=ciphers[k], default=True, enable_events=True))
        ls = create_columns(ls, k, 5)
    return ls

def format_url(url):
    # Check if the URL starts with 'http://' or 'https://'
    if not url.startswith(('http://', 'https://')):
        # Add 'https://' prefix if missing
        url = 'https://' + url
    # Check if the URL has a valid format
    if not re.match(r'^https?://\w+', url):
        # Return None if the URL is invalid
        return None
    return url

def try_request(url: str, session: type(requests.Session) = requests):
    try:
        return session.get(url)
    except requests.exceptions.RequestException as e:
        print(e)
        return False

def get_soup(data, selected_option: str = 'html.parser'):
    try:
        soup = change_glob('last_soup', BeautifulSoup(data, selected_option))
    except:
        soup = None
    return soup

def get_parsed_html(url: str = 'https://www.example.com', header: str = create_user_agent()):
    s = requests.Session()
    s.cookies["cf_clearance"] = "cb4c883efc59d0e990caf7508902591f4569e7bf-1617321078-0-150"
    s.headers.update({"user-agent": get_user_agents()[0]})
    adapter = TLSAdapter(ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1)
    s.mount('https://', adapter)
    r = try_request(url=url, session=s)
    data = r.text
    if r is False:
        return None
    return data

def parse_all(data):
    ls_type, ls_tag, ls_class, ls_desc = [], [], [], []
    data = str(data).split('<')
    for k in range(1, len(data)):
        dat = data[k].split('>')[0]
        if dat[0] != '/':
            if dat.split(' ')[0] not in ls_type:
                ls_type.append(dat.split(' ')[0])
        dat = dat[len(dat.split(' ')[0]) + 1:].split('"')
        for c in range(1, len(dat)):
            if len(dat[c]) > 0:
                if '=' == dat[c][-1] and ' ' == dat[c][0] and dat[c] != '/':
                    if dat[c][1:] + '"' + dat[c + 1] + '"' not in ls_desc:
                        ls_desc.append(dat[c][1:] + '"' + dat[c + 1] + '"')
                    if dat[c][1:-1] not in ls_tag:
                        ls_tag.append(dat[c][1:-1])
                    if dat[c + 1] not in ls_class:
                        ls_class.append(dat[c + 1])
    return ls_type, ls_desc, ls_tag, ls_class

def parse_react_source(data):
    soup = BeautifulSoup(data, 'html.parser')
    script_tags = soup.find_all('script', type=lambda t: t and ('javascript' in t or 'jsx' in t))
    react_source_code = []
    for script_tag in script_tags:
        react_source_code.append(script_tag.string)
    return react_source_code

def all_soup(data, tag, typ, clas, inp):
    print(getattr(last_soup, tag, typ))  # ,string))
    return getattr(last_soup, tag, typ)

def find_all_soup(string: str):
    return last_soup.find_all(string)

def get_bs4_options():
    bs4_options = [
        'BeautifulSoup',
        'Tag',
        'NavigableString',
        'Comment',
        'ResultSet',
        'SoupStrainer',
        'CData'
    ]
    descriptions = [
        'The main BeautifulSoup class used for parsing HTML.',
        'Represents an HTML tag.',
        'Represents a string within an HTML document.',
        'Represents an HTML comment.',
        'Represents a collection of tags found during a search.',
        'Allows parsing only a specific subset of the HTML document.',
        'Represents a CDATA section within an XML document.'
    ]
    return list(zip(bs4_options, descriptions))

def mk_component(ls, component_ls):
    for k in range(0, len(component_ls)):
        ls.append(component_ls[k])
    return ls

def mk_horizontal(component, ls: list = []):
    ls.append(component)
    return ls

def mk_vertical(component, ls: list = []):
    ls.append([component])
    return ls

def get_input_text():
    component = get_gui_fun(name='Frame', args={'title': '', "layout": [get_gui_fun(name='Input', args={"key": "-URL_INPUT-", "enable_events": True}), get_gui_fun(name='Text', args={"key": "-URL_FORMAT-", "enable_events": True})]})
    return mk_vertical(component)

def get_parser_choices():
    return ['html.parser', 'lxml', 'html5lib']

def get_status(url):
    return try_request(url=url).status_code

def get_multi_line(args):
    return [get_gui_fun(name='Multiline', args={**args, **expandable()})]

def get_url_frame(key, type: str = "Text"):
    return get_gui_fun('Frame', {'title': key, 'layout': [[get_gui_fun(type, {'text': key, "key": f"-URL_{key}-", "enable_events": True})]]})

def get_check_frame(key):
    return [get_gui_fun('Checkbox', {'text': '', "default": True, "key": f'-CHECK_{key}-', "enable_events": True}),
            get_gui_fun('Combo', {"values": [], "size": (15, 1), "key": f'-SOUP_{key}-', "enable_events": True})]

def get_find_soup_frame():
    return [sg.Frame('find soup', [get_check_frame('TAG'), get_check_frame('ELEMENT'), get_check_frame('TYPE'), get_check_frame('CLASS'),
                                  [sg.Button('find soup'), sg.Button('all soup')]])]

def get_url_input_frame():
    return [
        mk_component([], [
            get_url_frame('INPUT', type='Input'),
            get_url_frame('FORMATTED'),
            get_url_frame('URL'),
            get_url_frame('STATUS'),
            get_url_frame('WARNING'),
            [sg.Button('formatted url',key='-CORRECT_URL-',visible=False)]
        ])
    ]

def get_parsing_options():
    return [sg.Text('Parsing Capabilities:', size=(15, 1)), sg.DropDown(get_parser_choices(), default_value='html.parser', key='-PARSER-', enable_events=True)]

def get_user_agent_frame():
    return [sg.Checkbox('Custom User-Agent', default=False, key='-CUSTOMUA-', enable_events=True)], [sg.Text('User-Agent:', size=(8, 1)), sg.Combo(get_user_agents(), default_value=get_user_agents()[0], key='-USERAGENT-', disabled=False)]

def get_source_layout():
    layout = [
        get_url_input_frame(),
        get_user_agent_frame(),
        [sg.Button('Grab URL'), sg.Button('Action')],
        get_multi_line({"key": "-SOURCECODE-"}),
        get_parsing_options(),
        get_multi_line({"key": "-SOUP_OUTPUT-"}),
        get_find_soup_frame(),
        get_multi_line({"key": "-FIND_ALL_OUTPUT-"})]
    
    return layout
def update_status(window,js):
    for k in range(0,len(list(js.keys()))):
        window[list(js.keys())[k]].update(value=js[list(js.keys())[k]])
def while_source_top(window, event, values):
        if 'CHECK_' in event:
            if values[event] == True:
                globals()['curr_check'] = event.split('CHECK_')[1]
                keys = list(values.keys())
                for k in range(0, len(keys)):
                    key = keys[k]
                    if 'CHECK_' in key and key != event:
                        window[key].update(value=False)
        if event == 'all soup':
            window['-FIND_ALL_OUTPUT-'].update(value=find_all_soup(values[f'-SOUP_{globals()["curr_check"]}']))
        if event == 'get soup':
            window['-FIND_ALL_OUTPUT-'].update(value=all_soup(values['-SOUP_OUTPUT-'], values['-SOUP_TAG-'], values['-SOUP_TYPE-'], values['-SOUP_CLASS-'], values['-SOUP_INPUT-']))

        if event == '-URL_INPUT-':
            url = format_url(values['-URL_INPUT-'])
            if url == None:
                url = ''
            try:
                r = requests.get(url)
                window['-CORRECT_URL-'].update(visible=True)
                js_valid = {"-URL_FORMATTED-":url,"-URL_WARNING-":'valid','-URL_STATUS-':r.status_code,'-URL_URL-':True}
            except:
                window['-CORRECT_URL-'].update(visible=False)
                js_valid = {"-URL_FORMATTED-":url,"-URL_WARNING-":'invalid','-URL_STATUS-':'fail','-URL_URL-':False}
            update_status(window,js_valid)     
        if event == 'formatted url':
            window['-URL_INPUT-'].update(value=format_url(values['-URL_INPUT-']))
        if event == '-CUSTOMUA-':
            window['-SOURCECODE-'].update(disabled=values['-CUSTOMUA-'])
            if not values['-CUSTOMUA-']:
                window['-USERAGENT-'].update(value=get_user_agents()[0])
                window['-USERAGENT-'].update(disabled=True)
            else:
                window['-USERAGENT-'].update(disabled=False)
        if event in get_ciphers():
            ls = []
            for k in range(len(get_ciphers())):
                if values[get_ciphers()[k]] == True:
                    ls.append(get_ciphers()[k])
            window['-CIPHERS_OUTPUT-'].update(value=create_ciphers_string(ls=ls))
        if event == '-PARSER-':
            display_soup(window, values, source_code)

def display_soup(window, values, source_code):
    soup = get_soup(data=source_code, selected_option=values['-PARSER-'])
    if soup != None:
        window['-SOUP_OUTPUT-'].update(value=soup)
        ls_type, ls_desc, ls_tag, ls_class = parse_all(soup)
        window['-SOUP_TAG-'].update(values=ls_type, value=ls_type[0])
        if len(ls_desc) > 0:
            window['-SOUP_ELEMENT-'].update(values=ls_desc, value=ls_desc[0])
        if len(ls_tag) > 0:
            window['-SOUP_TYPE-'].update(values=ls_tag, value=ls_tag[0])
        if len(ls_class) > 0:
            window['-SOUP_CLASS-'].update(values=ls_class, value=ls_class[0])

def while_action(window, event, values):
    if event == 'Action':
        source_code = window['-SOURCECODE-'].get()
        selected_option = values['-PARSER-']
        soup = display_soup(window, values, source_code)
        window['-SOURCECODE-'].update(value=source_code)
        if selected_option == 'BeautifulSoup':
            result = soup
        elif selected_option == 'Tag':
            result = soup.find('tag_name')
        elif selected_option == 'NavigableString':
            result = soup.find('tag_name').string
        elif selected_option == 'Comment':
            result = soup.find(text=lambda text: isinstance(text, Comment))
        elif selected_option == 'ResultSet':
            result = soup.find_all('tag_name')
        elif selected_option == 'SoupStrainer':
            result = BeautifulSoup(source_code, 'html.parser', parse_only=SoupStrainer('tag_name'))
        elif selected_option == 'CData':
            result = soup.find(text=lambda text: isinstance(text, CData))
        else:
            result = None
        window['-OUTPUT-'].update(value=str(result))
def while_grab_url(window, event, values):
    if event == 'Grab URL':
        formatted_url = format_url(values['-URL_INPUT-'])
        if formatted_url:
            source_code = get_parsed_html(url=formatted_url, header=create_user_agent(values['-CUSTOMUA-']))
            window['-SOURCECODE-'].update(value=source_code)
            display_soup(window, values, source_code)
        else:
            sg.popup('Invalid URL format. Please enter a valid URL.')
        user_agent = values['-USERAGENT-']
        source_code = get_parsed_html(url=formatted_url, header=create_user_agent(values['-CUSTOMUA-']))
        window['-SOURCECODE-'].update(value=source_code)
        display_soup(window, values, source_code)
def url_grabber_component():
    globals()['curr_check'] = 'TAG-'
    globals()['URL_CURRENT'] = 'www.example.com'
    layout = get_source_layout()
    window = get_gui_fun(name='Window', args={'title': 'URL Grabber', 'layout': layout, **expandable()})
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
            window.close()
        while_source_top(window, event, values)
        while_grab_url(window, event, values)
        while_action(window, event, values)
def get_parsed_html(url: str = 'https://www.example.com', header: str = create_user_agent()):
    s = requests.Session()
    s.cookies["cf_clearance"] = "cb4c883efc59d0e990caf7508902591f4569e7bf-1617321078-0-150"
    s.headers.update({"user-agent": get_user_agents()[0]})
    adapter = TLSAdapter(ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1)
    s.mount('https://', adapter)
    r = try_request(url=url, session=s)
    data = r.text
    if r is False:
        return None
    return data
url_grabber_component()
