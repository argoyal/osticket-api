import hashlib
import uuid
import time
from database import db
from datetime import datetime
from services.exceptions import ServiceException


class APIKeyService(object):
    """
    all the services related to api keys
    are present here.

    Note: the usage of api key is pretty limited
    with osticket currently. the authentication process
    for our system will therefor check the request ip address
    as mentioned against the api key and also check for
    the header parameter Authorization: Bearer <API_Key>.

    We won't be using special options i.e. Can create ticket
    etc and these API keys will override those specific options

    Work needed: We can actually use JWT's as a future prospect
    and is actually a better option.

    logic for generation of API Key from the codebase: --->
    ===================================================================
        strtoupper(md5(time().$vars['ipaddr'].md5(Misc::randCode(16))))
    ===================================================================

    ** avoiding the 16 digit random code generator and using simple
    python uuid functions.
    """

    def create_apikey(self, ip_address, isactive=1, notes='',
                      can_create_tickets=0, can_exec_cron=0):
        """
        creates the api key

        uses the hardcoded values for can_create_tickets, can_exec_cron
        as 0
        """

        uid = uuid.uuid4()
        random_string = str(uid.hex[:16])
        random_hex = hashlib.md5(random_string.encode("utf-8")).hexdigest()

        api_key = hashlib.md5(
            '{}.{}.{}'.format(
                time.time(), ip_address, random_hex
            ).encode('utf-8')).hexdigest().upper()

        query_template = """
            INSERT INTO ost_api_key (
                isactive, ipaddr, apikey, can_create_tickets, can_exec_cron,
                notes, updated, created
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        cur = db.cursor()

        cur.execute(query_template, (isactive, ip_address, api_key,
                                     can_create_tickets, can_exec_cron, notes,
                                     datetime.now(), datetime.now()))

        cur.close()

        try:
            db.commit()

            return api_key
        except Exception as exc:
            db.rollback()
            raise ServiceException(exc.message)

    def make_apikey_inactive(self, api_key):
        """
        marks the api key inactive so that one cannot use it
        """

        query_template = """
            UPDATE ost_api_key SET isactive=0, updated={} WHERE apikey={}
        """

        cur = db.cursor()

        cur.execute(query_template.format(datetime.now(), api_key))

        cur.close()

        try:
            db.commit()
        except Exception as exc:
            db.rollback()
            raise ServiceException(exc.message)

    def is_apikey_valid(self, api_key, ip_address):
        """
        checks the availability of api key and whether
        this can be used for API calls.
        """

        query_template = """
            SELECT * FROM ost_api_key WHERE apikey=%s
        """

        cur = db.cursor()

        cur.execute(query_template, (api_key,))

        data = cur.fetchone()

        cur.close()

        if not data:
            return False

        if not data.get("ipaddr") == ip_address:
            return False

        if not data.get("isactive") == 1:
            return False

        return True
