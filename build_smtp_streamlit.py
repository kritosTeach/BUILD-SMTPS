import streamlit as st
import re
import sys
import os
import json
import socket


from datetime import datetime

# ============================
# SMTP database (same as build_smtp.py)
# ============================
TIMEOUT = 8
THREADS = 20
DEFAULT_PORT = 465

SMTP_DATABASE = {
    'gmail.com': {'host': 'smtp.gmail.com', 'port': 465, 'ssl': True},
    'googlemail.com': {'host': 'smtp.gmail.com', 'port': 465, 'ssl': True},

    'yahoo.com': {'host': 'smtp.mail.yahoo.com', 'port': 465, 'ssl': True},
    'yahoo.es': {'host': 'smtp.mail.yahoo.com', 'port': 465, 'ssl': True},
    'yahoo.fr': {'host': 'smtp.mail.yahoo.com', 'port': 465, 'ssl': True},
    'yahoo.co.uk': {'host': 'smtp.mail.yahoo.com', 'port': 465, 'ssl': True},
    'ymail.com': {'host': 'smtp.mail.yahoo.com', 'port': 465, 'ssl': True},
    'rocketmail.com': {'host': 'smtp.mail.yahoo.com', 'port': 465, 'ssl': True},

    'outlook.com': {'host': 'smtp.office365.com', 'port': 587, 'ssl': False},
    'hotmail.com': {'host': 'smtp.office365.com', 'port': 587, 'ssl': False},
    'hotmail.fr': {'host': 'smtp.office365.com', 'port': 587, 'ssl': False},
    'live.com': {'host': 'smtp.office365.com', 'port': 587, 'ssl': False},
    'live.fr': {'host': 'smtp.office365.com', 'port': 587, 'ssl': False},
    'msn.com': {'host': 'smtp.office365.com', 'port': 587, 'ssl': False},
    'passport.com': {'host': 'smtp.office365.com', 'port': 587, 'ssl': False},

    'orange.fr': {'host': 'smtp.orange.fr', 'port': 465, 'ssl': True},
    'orange.net': {'host': 'smtp.orange.net', 'port': 465, 'ssl': True},
    'wanadoo.fr': {'host': 'smtp.orange.fr', 'port': 465, 'ssl': True},

    'libero.it': {'host': 'mail.libero.it', 'port': 465, 'ssl': True},
    'virgilio.it': {'host': 'mail.libero.it', 'port': 465, 'ssl': True},

    'web.de': {'host': 'smtp.web.de', 'port': 587, 'ssl': False},
    'gmx.de': {'host': 'mail.gmx.net', 'port': 587, 'ssl': False},
    'gmx.net': {'host': 'mail.gmx.net', 'port': 587, 'ssl': False},
    'gmx.ch': {'host': 'mail.gmx.net', 'port': 587, 'ssl': False},

    'aol.com': {'host': 'smtp.aol.com', 'port': 587, 'ssl': False},

    'comcast.net': {'host': 'smtp.comcast.net', 'port': 587, 'ssl': False},

    'verizon.net': {'host': 'outgoing.verizon.net', 'port': 465, 'ssl': True},

    'virginmedia.com': {'host': 'smtp.virginmedia.com', 'port': 587, 'ssl': False},
    'virgin.net': {'host': 'smtp.virgin.net', 'port': 587, 'ssl': False},

    'talktalk.net': {'host': 'smtp.talktalk.net', 'port': 587, 'ssl': False},

    'btconnect.com': {'host': 'mail.btconnect.com', 'port': 587, 'ssl': False},
    'btinternet.com': {'host': 'mail.btinternet.com', 'port': 587, 'ssl': False},

    'tiscali.co.uk': {'host': 'smtp.tiscali.co.uk', 'port': 587, 'ssl': False},
    'tiscali.it': {'host': 'smtp.tiscali.it', 'port': 587, 'ssl': False},

    'free.fr': {'host': 'smtp.free.fr', 'port': 587, 'ssl': False},

    'sfr.fr': {'host': 'smtp.sfr.fr', 'port': 465, 'ssl': True},

    'laposte.net': {'host': 'smtp.laposte.net', 'port': 587, 'ssl': False},

    'freenet.de': {'host': 'mx.freenet.de', 'port': 587, 'ssl': False},

    't-online.de': {'host': 'smtp.t-online.de', 'port': 587, 'ssl': False},

    '1und1.de': {'host': 'smtp.1und1.de', 'port': 587, 'ssl': False},
    'ionos.de': {'host': 'smtp.ionos.de', 'port': 587, 'ssl': False},

    'earthlink.net': {'host': 'smtpauth.earthlink.net', 'port': 587, 'ssl': False},

    'mail.ru': {'host': 'smtp.mail.ru', 'port': 465, 'ssl': True},
    'bk.ru': {'host': 'smtp.mail.ru', 'port': 465, 'ssl': True},
    'list.ru': {'host': 'smtp.mail.ru', 'port': 465, 'ssl': True},
    'inbox.ru': {'host': 'smtp.mail.ru', 'port': 465, 'ssl': True},

    'yandex.com': {'host': 'smtp.yandex.com', 'port': 465, 'ssl': True},
    'yandex.ru': {'host': 'smtp.yandex.ru', 'port': 465, 'ssl': True},
    'ya.ru': {'host': 'smtp.yandex.ru', 'port': 465, 'ssl': True},

    'qq.com': {'host': 'smtp.qq.com', 'port': 465, 'ssl': True},
    'foxmail.com': {'host': 'smtp.qq.com', 'port': 465, 'ssl': True},

    '163.com': {'host': 'smtp.163.com', 'port': 465, 'ssl': True},
    '126.com': {'host': 'smtp.126.com', 'port': 465, 'ssl': True},
    'yeah.net': {'host': 'smtp.yeah.net', 'port': 465, 'ssl': True},

    'sina.com': {'host': 'smtp.sina.com', 'port': 465, 'ssl': True},
    'sina.cn': {'host': 'smtp.sina.cn', 'port': 465, 'ssl': True},

    'rediffmail.com': {'host': 'smtp.rediffmail.net', 'port': 587, 'ssl': False},
    'rediffmail.net': {'host': 'smtp.rediffmail.net', 'port': 587, 'ssl': False},

    'zoho.com': {'host': 'smtp.zoho.com', 'port': 465, 'ssl': True},
    'zohomail.com': {'host': 'smtp.zoho.com', 'port': 465, 'ssl': True},

    'fastmail.com': {'host': 'smtp.fastmail.com', 'port': 465, 'ssl': True},
    'fastmail.fm': {'host': 'smtp.fastmail.fm', 'port': 465, 'ssl': True},

    'posteo.de': {'host': 'smtp.posteo.de', 'port': 465, 'ssl': True},
    'posteo.net': {'host': 'smtp.posteo.net', 'port': 465, 'ssl': True},

    'runbox.com': {'host': 'mail.runbox.com', 'port': 587, 'ssl': False},

    'arcor.de': {'host': 'smtp.arcor.de', 'port': 587, 'ssl': False},

    'tin.it': {'host': 'mail.tin.it', 'port': 465, 'ssl': True},
    'alice.it': {'host': 'mail.alice.it', 'port': 465, 'ssl': True},
    'aliceadsl.fr': {'host': 'smtp.aliceadsl.fr', 'port': 587, 'ssl': False},

    'zonnet.nl': {'host': 'smtp.zonnet.nl', 'port': 587, 'ssl': False},
    'hetnet.nl': {'host': 'smtp.hetnet.nl', 'port': 587, 'ssl': False},
    'kpnmail.nl': {'host': 'smtp.kpnmail.nl', 'port': 587, 'ssl': False},

    'skynet.be': {'host': 'smtp.skynet.be', 'port': 587, 'ssl': False},
    'telenet.be': {'host': 'smtp.telenet.be', 'port': 587, 'ssl': False},

    'bluewin.ch': {'host': 'smtpauths.bluewin.ch', 'port': 587, 'ssl': False},
    'swissonline.ch': {'host': 'smtpauths.bluewin.ch', 'port': 587, 'ssl': False},

    'iinet.net.au': {'host': 'mail.iinet.net.au', 'port': 587, 'ssl': False},
    'bigpond.com': {'host': 'smtp.bigpond.com', 'port': 587, 'ssl': False},
    'optusnet.com.au': {'host': 'smtp.optusnet.com.au', 'port': 587, 'ssl': False},
    'tpg.com.au': {'host': 'smtp.tpg.com.au', 'port': 587, 'ssl': False},

    'xtra.co.nz': {'host': 'smtp.xtra.co.nz', 'port': 587, 'ssl': False},

    'hi-ho.ne.jp': {'host': 'smtp.hi-ho.ne.jp', 'port': 465, 'ssl': True},
    'nifty.com': {'host': 'smtp.nifty.com', 'port': 465, 'ssl': True},
    'so-net.ne.jp': {'host': 'smtp.so-net.ne.jp', 'port': 465, 'ssl': True},
    'ocn.ne.jp': {'host': 'smtp.ocn.ne.jp', 'port': 465, 'ssl': True},
    'zaq.ne.jp': {'host': 'smtp.zaq.ne.jp', 'port': 465, 'ssl': True},

    'poczta.fm': {'host': 'smtp.poczta.fm', 'port': 587, 'ssl': False},
    'poczta.onet.pl': {'host': 'smtp.poczta.onet.pl', 'port': 587, 'ssl': False},
    'wp.pl': {'host': 'smtp.wp.pl', 'port': 587, 'ssl': False},
    'o2.pl': {'host': 'smtp.poczta.o2.pl', 'port': 587, 'ssl': False},

    'seznam.cz': {'host': 'smtp.seznam.cz', 'port': 587, 'ssl': False},
    'email.cz': {'host': 'smtp.email.cz', 'port': 587, 'ssl': False},

    'eyou.com': {'host': 'smtp.eyou.com', 'port': 25, 'ssl': False},
    'sogou.com': {'host': 'smtp.sogou.com', 'port': 465, 'ssl': True},
    'tom.com': {'host': 'smtp.tom.com', 'port': 465, 'ssl': True},

    'rambler.ru': {'host': 'smtp.rambler.ru', 'port': 465, 'ssl': True},

    'uol.com.br': {'host': 'smtp.uol.com.br', 'port': 587, 'ssl': False},
    'bol.com.br': {'host': 'smtp.bol.com.br', 'port': 587, 'ssl': False},
    'ig.com.br': {'host': 'smtp.ig.com.br', 'port': 587, 'ssl': False},
    'globo.com': {'host': 'smtp.globo.com', 'port': 587, 'ssl': False},

    'telefonica.net': {'host': 'smtp.telefonica.net', 'port': 587, 'ssl': False},
    'ono.com': {'host': 'smtp.ono.com', 'port': 587, 'ssl': False},
    'terra.es': {'host': 'smtp.terra.es', 'port': 587, 'ssl': False},
    'eircom.net': {'host': 'smtp.eir.ie', 'port': 587, 'ssl': False},
    'eir.ie': {'host': 'smtp.eir.ie', 'port': 587, 'ssl': False},
    'o2.co.uk': {'host': 'smtp.o2.co.uk', 'port': 587, 'ssl': False},
    'o2online.de': {'host': 'smtp.o2online.de', 'port': 587, 'ssl': False},

    'protonmail.com': {'host': '127.0.0.1', 'port': 1025, 'ssl': False, 'note': 'ProtonMail Bridge required'},
    'protonmail.ch': {'host': '127.0.0.1', 'port': 1025, 'ssl': False, 'note': 'ProtonMail Bridge required'},
    'pm.me': {'host': '127.0.0.1', 'port': 1025, 'ssl': False, 'note': 'ProtonMail Bridge required'},
}


# ============================
# Parsing & conversion (same behavior)
# ============================

def parse_line(line: str):
    line = line.strip()
    if not line or line.startswith('#') or line.startswith('//'):
        return None

    # تجاهل الروابط (Telegram links etc)
    if 't.me' in line or 'https://' in line:
        email_match = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', line)
        if email_match:
            rest = line[line.find(email_match.group(1)) + len(email_match.group(1)) :]
            pass_match = re.search(r'[:](.+?)$', rest)
            if pass_match:
                return email_match.group(1), pass_match.group(1).strip()
        return None

    line = line.lstrip('@')

    if ':' in line:
        parts = line.split(':', 1)
        email = parts[0].strip()
        password = parts[1].strip()

        if '@' in email and '.' in email.split('@')[1]:
            password = password.rstrip(' ,;')
            return email, password

    return None


def get_domain(email: str):
    return email.split('@')[1].lower().strip()


def get_smtp_config(email: str):
    domain = get_domain(email)

    if domain in SMTP_DATABASE:
        return SMTP_DATABASE[domain].copy()

    # DNS/MX discovery disabled. Only try common hostnames with port probing.
    smtp_host = f"smtp.{domain}"
    if check_port(smtp_host, 465):
        return {'host': smtp_host, 'port': 465, 'ssl': True}

    alt_port = 587
    if check_port(smtp_host, alt_port):
        return {'host': smtp_host, 'port': alt_port, 'ssl': False}

    mail_host = f"mail.{domain}"
    if check_port(mail_host, 465):
        return {'host': mail_host, 'port': 465, 'ssl': True}

    if check_port(mail_host, alt_port):
        return {'host': mail_host, 'port': alt_port, 'ssl': False}

    return None



def check_port(host: str, port: int):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception:
        return False


def validate_smtp(email: str, password: str, config: dict):
    host = config['host']
    port = config['port']

    if not check_port(host, port):
        alt_port = 587 if port == 465 else 465
        if check_port(host, alt_port):
            config['port'] = alt_port
            config['ssl'] = (alt_port == 465)
            return config

    return config


def clean_credentials(email: str, password: str):
    email = email.lstrip('@')
    password = password.strip()
    password = re.sub(r'\s+$', '', password)
    return email, password


def convert_credentials_to_smtp(credentials, do_validate=False, do_dns=False, output_format='plain', filter_weak=False):

    converted = []
    failed = []
    unique_domains = set()
    domain_stats = {}

    for email, password in credentials:
        domain = get_domain(email)
        unique_domains.add(domain)
        domain_stats[domain] = domain_stats.get(domain, 0) + 1

        config = get_smtp_config(email)

        if config:
            if do_validate:
                config = validate_smtp(email, password, config)

            is_weak = False
            if password.lower() in [
                '123456', '12345', '123456789', 'password', 'qwerty', 'admin', 'letmein', 'welcome'
            ] or len(password) < 6:
                is_weak = True

            converted.append({
                'email': email,
                'password': password,
                'domain': domain,
                'smtp_host': config['host'],
                'smtp_port': config['port'],
                'ssl': config.get('ssl', False),
                'note': config.get('note', ''),
                'weak_password': is_weak,
            })
        else:
            failed.append({'email': email, 'password': password, 'domain': domain})

    # weak filter preview
    if filter_weak:
        converted = [c for c in converted if c['weak_password']]

    output_data = None
    return converted, failed, unique_domains, domain_stats


# ============================
# Streamlit UI
# ============================

st.set_page_config(page_title='SMTP Credentials Converter (Streamlit)', layout='wide')

st.markdown(
    """
    <style>
      body { background-color:#0e1117; color:#e6edf3; }
      .stApp { background-color:#0e1117; }
      input, textarea { background-color:#1a1c23 !important; color:#00ff41 !important; border:1px solid #00ff41 !important; }
      .stButton>button { background-color:#00ff41; color:#000; font-weight:800; }
      .stButton>button:hover { background-color:#00cc33; }
      .st-expander { border:1px solid #00ff41; border-radius:8px; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title('🧾 SMTP Credentials Converter')

with st.form('build_smtp_form'):
    st.subheader('📥 Input')

    input_mode = st.radio(
        'How to provide credentials?',
        options=['Paste in box', 'Upload file'],
        index=0,
        horizontal=True,
    )

    creds_text = ''
    uploaded = None

    if input_mode == 'Paste in box':
        creds_text = st.text_area(
            'Paste credentials (one per line: email:password or link containing email and password)',
            height=260,
            placeholder='user@example.com:pass123\nother@example.com:secret',
        )
    else:
        uploaded = st.file_uploader('Upload credentials.txt', type=['txt'], accept_multiple_files=False)
        if uploaded is not None:
            try:
                creds_text = uploaded.read().decode('utf-8', errors='ignore')
            except Exception:
                creds_text = ''

    st.subheader('⚙️ Options')
    do_dns = st.checkbox('Use DNS discovery (slower) [--dns]', value=False)
    do_validate = st.checkbox('Validate SMTP port open [--validate] (slower)', value=False)

    output_format = st.selectbox('Output format', options=['plain', 'json'], index=0)
    filter_weak = st.checkbox('Filter weak passwords only [--filter-weak]', value=False)

    submitted = st.form_submit_button('START CONVERT')

if submitted:
    # Parse credentials
    raw_lines = [ln.strip() for ln in creds_text.splitlines()]

    credentials = []
    skipped = 0
    for ln in raw_lines:
        if not ln:
            continue
        res = parse_line(ln)
        if res:
            email, password = res
            email, password = clean_credentials(email, password)
            credentials.append((email, password))
        else:
            skipped += 1

    if not credentials:
        st.error('No valid credentials found in input.')
        st.stop()

    st.info(f'✅ Parsed credentials: {len(credentials)} (skipped {skipped})')

    converted, failed, unique_domains, domain_stats = convert_credentials_to_smtp(
        credentials,
        do_validate=do_validate,
        do_dns=do_dns,
        output_format=output_format,
        filter_weak=filter_weak,
    )

    st.success(f'✅ Converted: {len(converted)} | ❌ Failed: {len(failed)} | unique domains: {len(unique_domains)}')

    # Save output
    out_name = 'smtp_converted_streamlit.txt' if output_format == 'plain' else 'smtp_converted_streamlit.json'

    if output_format == 'plain':
        with open(out_name, 'w', encoding='utf-8') as f:
            for c in converted:
                line = f"{c['smtp_host']}|{c['smtp_port']}|{c['email']}|{c['password']}"
                if filter_weak and c.get('weak_password'):
                    line += '  # WEAK PASSWORD'
                f.write(line + '\n')
    else:
        output_data = {
            'source_file': 'streamlit_input',
            'converted_at': datetime.now().isoformat(),
            'total': len(credentials),
            'success': len(converted),
            'failed': len(failed),
            'credentials': [],
        }
        for c in converted:
            entry = {
                'email': c['email'],
                'password': c['password'],
                'smtp': {
                    'host': c['smtp_host'],
                    'port': c['smtp_port'],
                    'ssl': c['ssl'],
                },
            }
            if c.get('note'):
                entry['smtp']['note'] = c['note']
            if c.get('weak_password'):
                entry['weak_password'] = True
            output_data['credentials'].append(entry)

        with open(out_name, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2)

    st.success(f'💾 Saved output to: {out_name}')

    # Preview + copy box
    st.subheader('🧾 Output (copy all)')
    if output_format == 'plain':
        output_lines = []
        for c in converted:
            line = f"{c['smtp_host']}|{c['smtp_port']}|{c['email']}|{c['password']}"
            if filter_weak and c.get('weak_password'):
                line += '  # WEAK PASSWORD'
            output_lines.append(line)
        output_text = "\n".join(output_lines)
        st.text_area('Copy output here', value=output_text, height=260)
        st.download_button(
            label='Download smtp_converted_streamlit.txt',
            data=output_text,
            file_name='smtp_converted_streamlit.txt',
            mime='text/plain',
        )
    else:
        output_text = json.dumps(output_data, indent=2)
        st.text_area('Copy JSON output here', value=output_text, height=260)
        st.download_button(
            label='Download smtp_converted_streamlit.json',
            data=output_text,
            file_name='smtp_converted_streamlit.json',
            mime='application/json',
        )

    st.divider()
    st.subheader('👀 Preview (first 20)')
    for i, c in enumerate(converted[:20], 1):
        ssl_tag = '🔒' if c['ssl'] else '🔓'
        st.write(f"{i}. {ssl_tag} {c['smtp_host']}|{c['smtp_port']}|{c['email']}|{c['password']}")

    if failed:
        st.subheader('❌ Failed (first 10)')
        for f in failed[:10]:
            st.write(f"- {f['email']} ({f['domain']})")


