from database import db
from datetime import datetime
from services.exceptions import ServiceException


class OrganizationService(object):
    """
    all the services related to organization
    are present here.
    """

    def get_organization(self, org_id):
        """
        returns the organization data given organization id
        """

        query_template = """
            SELECT * FROM ost_organization t1 INNER JOIN
             ost_organization__cdata t2 ON t2.org_id=t1.id
             WHERE t1.id=%s
        """

        cur = db.cursor()

        cur.execute(query_template, (org_id,))

        row = cur.fetchone()
        cur.close()

        return row

    def organization_exists(self, org_id):
        """
        checks for the existance of an organization
        """

        query_template = """
            SELECT EXISTS (SELECT 1 from ost_organization WHERE id=%s)
        """

        cur = db.cursor()
        cur.execute(query_template, (org_id,))

        result = cur.fetchone()
        cur.close()

        return bool(next(iter(result.values())))

    def add_organization(self, name, manager='', status=8, domain='',
                         extra=None, address='', phone='', website='',
                         notes=''):
        """
        creates an organization in the osticket database
        """

        def get_org_id_from_name():
            query_template = """
                SELECT id FROM ost_organization WHERE name=%s
            """

            cur = db.cursor()
            cur.execute(query_template, (name,))
            org_id = cur.fetchone().get("id")
            cur.close()

            return {"organization_id": org_id}

        query_template = """
            START TRANSACTION;
            BEGIN;
                INSERT INTO ost_organization
                (name, manager, status, domain, extra, created, updated)
                 VALUES (%s, %s, %s, %s, %s, %s, %s);

                SET @OrgID = LAST_INSERT_ID();

                INSERT INTO ost_organization__cdata
                (org_id, name, address, phone, website, notes)
                VALUES (@OrgID, %s, %s, %s, %s, %s);
            COMMIT;

            SELECT @OrgID;
        """

        cur = db.cursor()

        cur.execute(
            query_template, (
                name, manager, status, domain, extra,
                datetime.now(), datetime.now(), name, address, phone,
                website, notes
            ))

        cur.close()

        try:
            db.commit()
        except Exception as exc:
            db.rollback()
            raise ServiceException(exc.message)

        return get_org_id_from_name()

    def add_manager_to_organization(self, org_id, manager_id):
        """
        adds a manager to the organization
        """

        query_template = """
            UPDATE ost_organization SET manager=%s, updated=%s
             WHERE id=%s
        """

        cur = db.cursor()

        cur.execute(query_template, (manager_id, datetime.now(), org_id))

        cur.close()

        try:
            db.commit()
        except Exception as exc:
            db.rollback()
            raise ServiceException(exc.message)
