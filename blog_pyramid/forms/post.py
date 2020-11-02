import colander
import deform.widget
from slugify import slugify
from wtforms import Form, TextAreaField, validators

from blog_pyramid.models import Post, User
from blog_pyramid.models.category import Category


def get_categories(dbsession):
    all_categories = dbsession.query(Category).all()
    return [(category.name, category.name) for category in all_categories]


def get_users(dbsession):
    all_users = dbsession.query(User).all()
    return [(user.username, user.username) for user in all_users]


def validate_unique_title(node, appstruct, dbsession):
    if dbsession.query(Post).filter_by(slug=slugify(appstruct['title'])).first():
        raise colander.Invalid(node, "Post title already exists")


def get_post_form(dbsession, validator, user_role):
    class PostForm(colander.MappingSchema):
        title = colander.SchemaNode(colander.String(), title="Tytuł", validator=colander.Length(min=3, max=60))
        intro = colander.SchemaNode(colander.String(), title="Intro", widget=deform.widget.TextAreaWidget(),
                                    validator=colander.Length(min=10, max=200))
        body = colander.SchemaNode(colander.String(), title="Treść", widget=deform.widget.RichTextWidget(),
                                   validator=colander.Length(min=50))
        category = colander.SchemaNode(
            colander.String(),
            title="Kategoria",
            widget=deform.widget.SelectWidget(values=get_categories(dbsession)),
        )
        if user_role == 'admin':
            author = colander.SchemaNode(
                colander.String(),
                title="Author",
                widget=deform.widget.SelectWidget(values=get_users(dbsession)),
            )

    return PostForm(validator=validator)


def get_edit_post_form(dbsession):
    class PostEditForm(colander.MappingSchema):
        intro = colander.SchemaNode(colander.String(), title="Intro", widget=deform.widget.TextAreaWidget(),
                                    validator=colander.Length(min=10, max=200))
        body = colander.SchemaNode(colander.String(), title="Treść", widget=deform.widget.RichTextWidget(),
                                   validator=colander.Length(min=50))
        category = colander.SchemaNode(
            colander.String(),
            title="Kategoria",
            widget=deform.widget.SelectWidget(values=get_categories(dbsession)),
        )
    return PostEditForm()
