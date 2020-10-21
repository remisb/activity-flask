from activity.resource.restaurant import RestaurantListApi, RestaurantApi
from activity.resource.user import UserListApi, UserItemApi
from activity.resource.project import ProjectListApi, ProjectApi
from activity.resource.vote import VoteListApi, VoteApi
from activity.resource.auth import SignupApi, LoginApi


def register_routes(api, app, root="/api/v1"):
    api.add_resource(ProjectListApi, f'{root}/project')
    api.add_resource(ProjectApi, f"{root}/project/<int:project_id>")
    api.add_resource(RestaurantListApi, f"{root}/restaurant")
    api.add_resource(RestaurantApi, f"{root}/restaurant/<int:restaurant_id>")
    api.add_resource(UserListApi, f"{root}/user")
    api.add_resource(UserItemApi, f"{root}/user/<int:user_id>")
    api.add_resource(VoteListApi, f"{root}/vote")
    api.add_resource(VoteApi, f"{root}/vote/<int:restaurant_id>")
    api.add_resource(SignupApi, '/api/auth/signup')
    api.add_resource(LoginApi, '/api/auth/login')
