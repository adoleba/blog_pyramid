import colander
import deform.widget
from wtforms import Form, TextAreaField, validators

from blog_pyramid.models import Post
from blog_pyramid.models.category import Category


def get_categories(dbsession):
    all_categories = dbsession.query(Category).all()
    return [(category.name, category.name) for category in all_categories]


def validate_unique_title(node, appstruct, dbsession):
    if dbsession.query(Post).filter_by(title=appstruct['title']).first():
        raise colander.Invalid(node, "Post title already exists")


def get_post_form(dbsession, validator):
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
