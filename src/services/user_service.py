from services.exceptions import ServiceException
from services import OrganizationService
from database import db
from datetime import datetime
from utils import PasswordHash


org_service = OrganizationService()
hasher = PasswordHash(8, False)


class UserService(object):
    """
    all the services related to users are present
    here.

    Note: User has many fields that can be added as a
    support here, the bare minimum logic is implemented, which
    will create the user. The rest can be updated from the platform
    itself. If you still wish to add certain fields using api
    override the create_user function and you can get going

    Since I was implementing this for my own purpose I did not
    use username as a required parameter and have implemented
    username as a non required field for the service function.
    it is basically defaulted to email if not provided.
    """

    def get_user(self, email=None, username=None, uid=None):
        """
        gets the user details from different user tables
        in a single query.
        """

        EXCLUDE_FIELDS = ["passwd"]

        if not any([email, username, uid]):
            raise ServiceException('one of email, username or uid is needed')

        cur = db.cursor()

        if uid:
            query_template = """
                SELECT * FROM ost_user t1
                 INNER JOIN ost_user__cdata t2 ON t2.user_id=t1.id
                 INNER JOIN ost_user_email t3 ON t3.user_id=t1.id
                 INNER JOIN ost_user_account t4 ON t4.user_id=t1.id
                 WHERE t1.id=%s
            """

            cur.execute(query_template, (uid,))

        elif username:
            query_template = """
                SELECT * FROM ost_user_account t1
                 INNER JOIN ost_user__cdata t2 ON t2.user_id=t1.user_id
                 INNER JOIN ost_user_email t3 ON t3.user_id=t1.user_id
                 INNER JOIN ost_user t4 ON t4.id=t1.user_id
                 WHERE t1.username=%s
            """

            cur.execute(query_template, (username,))

        elif email:
            query_template = """
                SELECT * FROM ost_user_email t1
                 INNER JOIN ost_user t2 ON t2.default_email_id=t1.id
                 INNER JOIN ost_user__cdata t3 ON t3.user_id=t2.id
                 INNER JOIN ost_user_account t4 ON t4.user_id=t2.id
                 WHERE t1.address=%s
            """

            cur.execute(query_template, (email,))

        data = cur.fetchone()

        if not data:
            return data

        for field in EXCLUDE_FIELDS:
            data.pop(field)

        cur.close()

        return data

    def attach_user_to_organization(self, uid, org_id):
        """
        attaches a user in the user directory to a particular organization
        """
        if not org_service.organization_exists(org_id):
            raise ServiceException('No organization exists for given org_id')

        query_template = """
            UPDATE ost_user SET org_id=%s, updated=%s
             WHERE id=%s
        """

        cur = db.cursor()
        cur.execute(query_template, (org_id, datetime.now(), uid))
        cur.close()

        try:
            db.commit()
        except Exception as exc:
            db.rollback()
            raise ServiceException(exc.message)

    def add_user(self, email, name, password, org_id, phone='',
                 username=''):
        """
        adding user to the database
        ===============================================================
                            HARDCODED ENTRIES
        ===============================================================
        ost_user -> status value is set to 0. need to figure out what it
        does

        ost_user_account -> status value is set to 1. there are many other
        status values but 1 signifies user is Active/Registered to the
        platform and can actually use the platform. There are many other
        status values which can be used in a separate function that
        updates its values. need to implement as per business logic.

        ost_user_email -> flags value is set to 0 by default. need to figure
        out what it does.
        """

        def get_user_id_from_email():
            query_template = """
                SELECT user_id FROM ost_user_email WHERE address=%s
            """

            cur = db.cursor()
            cur.execute(query_template, (email,))
            user_id = cur.fetchone().get("user_id")
            cur.close()

            return {"user_id": user_id}

        user_data = self.get_user(email=email)

        if user_data:
            raise ServiceException('User with this email already exists')

        username = username or email
        hashed_password = hasher.hash_password(password)
        current_date = datetime.now()

        query_template = """
            START TRANSACTION;
                INSERT INTO ost_user
                (org_id, default_email_id, status, name, created, updated)
                 VALUES (%s, 0, 0, %s, %s, %s);

                SET @UserID = LAST_INSERT_ID();

                INSERT INTO ost_user_account
                 (user_id, status, username, passwd, registered)
                 VALUES (@UserID, 1, %s, %s, %s);

                INSERT INTO ost_user__cdata
                 (user_id, email, name, phone) VALUES
                 (@UserID, %s, %s, %s);

                INSERT INTO ost_user_email
                 (user_id, flags, address) VALUES
                 (@UserID, 0, %s);

                UPDATE ost_user SET default_email_id=LAST_INSERT_ID()
                 WHERE id=@UserID;
            COMMIT;
        """

        cur = db.cursor()

        cur.execute(query_template, (org_id, name, current_date,
                                     current_date, username, hashed_password,
                                     current_date, email, name, phone, email))

        cur.close()

        try:
            db.commit()
        except Exception as exc:
            db.rollback()
            raise ServiceException(exc.message)

        return get_user_id_from_email()
