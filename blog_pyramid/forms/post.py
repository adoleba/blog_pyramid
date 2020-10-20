import colander
import deform.widget
from blog_pyramid.models.category import Category


def get_categories(dbsession):
    all_categories = dbsession.query(Category).all()
    return [(category.name, category.name) for category in all_categories]


def get_post_form(dbsession):
    class PostForm(colander.MappingSchema):
        title = colander.SchemaNode(colander.String(), title="Tytuł", validator=colander.Length(min=3, max=30))
        intro = colander.SchemaNode(colander.String(), title="Intro", validator=colander.Length(min=10, max=100))
        body = colander.SchemaNode(colander.String(), title="Treść", widget=deform.widget.RichTextWidget(),
                                   validator=colander.Length(min=50))
        category = colander.SchemaNode(
            colander.String(),
            title="Kategoria",
            widget=deform.widget.SelectWidget(values=get_categories(dbsession)),
        )
    return PostForm()
