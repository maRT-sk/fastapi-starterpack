from starlette_admin import CustomView

home_view = CustomView(
    label="Dashboard",
    icon="fa fa-dashboard",
    path="/home",
    template_path="home.html",
)
