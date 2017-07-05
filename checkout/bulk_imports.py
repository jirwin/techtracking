from typing import List

from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget

from checkout.models import Team, Subject, User, Site, SKU, SKUType

SITE_PSEUDO_COLUMN = 'resolved_site'


class TeamResource(resources.ModelResource):
    subject = fields.Field(
        column_name='subject',
        attribute='subject',
        widget=ForeignKeyWidget(Subject, 'name'))

    members = fields.Field(
        column_name='members',
        attribute='members',
        widget=ManyToManyWidget(User, ',', 'name'))

    class Meta:
        model = Team
        fields = ('subject', 'members')

    def before_import_row(self, row, **kwargs):
        row[SITE_PSEUDO_COLUMN] = kwargs['user'].site

    def get_instance(self, instance_loader, row):
        subject = self.get_subject(row)
        members = self.get_members(row)

        team_qs = Team.objects.filter(site=row[SITE_PSEUDO_COLUMN], subject=subject)
        for member in members:
            team_qs = team_qs.filter(members__email=member.email)

        return team_qs.first()

    def init_instance(self, row=None):
        subject = self.get_subject(row)
        members = self.get_members(row)

        team: Team = Team.objects.create(subject=subject, site=row[SITE_PSEUDO_COLUMN])
        for member in members:
            team.members.add(member)

        team.save()
        return team

    @staticmethod
    def get_members(row) -> List[User]:
        members_str = None

        if 'Members' in row:
            members_str = row['Members']
        if 'members' in row:
            members_str = row['members']

        if not members_str:
            user_columns = list(row.keys())
            if SITE_PSEUDO_COLUMN in user_columns:
                user_columns.remove(SITE_PSEUDO_COLUMN)
            raise ValueError("Could not find column 'members' in first row - . Found: {}".format(user_columns))

        member_names: List[str] = members_str.split(",")

        members = []
        for member_name in member_names:
            member = row[SITE_PSEUDO_COLUMN].user_set.filter(name__icontains=member_name.strip()).first()

            if member is None:
                raise ValueError("{} not found in list of users at {}. Please enter one of: {}".format(
                    member_name,
                    row[SITE_PSEUDO_COLUMN].name,
                    ", ".join(["'" + user.get_full_name() + "'" for user in row[SITE_PSEUDO_COLUMN].user_set.all()])))

            members.append(member)

        return members

    @staticmethod
    def get_subject(row) -> Subject:
        subject_str = None

        if 'Subject' in row:
            subject_str = row['Subject']
        if 'subject' in row:
            subject_str = row['subject']

        if not subject_str:
            user_columns = list(row.keys())
            if 'resolved_site' in user_columns:
                user_columns.remove(SITE_PSEUDO_COLUMN)
            raise ValueError("Could not find column 'subject' in first row - . Found: {}".format(user_columns))

        subject: Subject = Subject.objects.filter(name__icontains=subject_str).first()
        if subject is None:
            raise ValueError("Subject {} not found in database. Please enter one of: {}".format(
                subject_str,
                ", ".join(["'" + subject.name + "'" for subject in Subject.objects.all()])))

        return subject


class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = ('site', 'is_staff', 'email', 'name')
        import_id_fields = ('email',)

    site = fields.Field(
        column_name='site',
        attribute='site',
        widget=ForeignKeyWidget(Site, 'name'))

    def before_import_row(self, row, **kwargs):
        user: User = kwargs['user']

        if row['site'] is None:
            row['site'] = user.site.name

        if not user.is_superuser:
            if row['is_staff'] != 1:
                row['is_staff'] = 0

            if row['site'] != user.site.name:
                raise ValueError("Cannot import users for site '{}', only '{}'".format(row['site'], user.site))

    def skip_row(self, instance, original):
        return original == instance

    def after_save_instance(self, user: User, using_transactions, dry_run):
        if not dry_run and not user.has_usable_password():
                user.send_welcome_email()


class SKUResource(resources.ModelResource):
    class Meta:
        model = SKU
        fields = ('id', 'type', 'model_identifier', 'display_name', 'units')

    type = fields.Field(
        column_name='type',
        attribute='type',
        widget=ForeignKeyWidget(SKUType, 'name'))
