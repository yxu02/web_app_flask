from flask_restful import Resource
from flask import request, send_file
from flask_uploads import UploadNotAllowed
from flask_jwt_extended import jwt_required, get_jwt_identity
import traceback, os
from libs import image_helper
from schemas.image import ImageSchema
from libs.strings import gettext

image_schema = ImageSchema()


class ImageUpload(Resource):

    @jwt_required
    def post(self):
        data = image_schema.load(request.files)
        user_id = get_jwt_identity()
        folder = f"user_{user_id}"

        try:
            image_path = image_helper.save_image(data["image"], folder)
            basename = image_helper.get_basename(image_path)
            return {"message": gettext("image_uploaded").format(basename)}, 201
        except UploadNotAllowed:  # forbidden file type
            extension = image_helper.get_extension(data["image"])
            return {"message": gettext("image_illegal_extension").format(extension)}, 400


class Image(Resource):
    @jwt_required
    def get(self, filename: str):
        """
        This endpoint returns the requested image if exists. It will use JWT to
        retrieve user information and look for the image inside the user's folder.
        """
        user_id = get_jwt_identity()
        folder = f"user_{user_id}"
        # check if filename is URL secure
        if not image_helper.is_filename_safe(filename):
            return {"message": gettext("image_illegal_file_name").format(filename)}, 400
        try:
            # try to send the requested file to the user with status code 200
            return send_file(image_helper.get_path(filename, folder=folder))
        except FileNotFoundError:
            return {"message": gettext("image_not_found").format(filename)}, 404

    @jwt_required
    def delete(self, filename: str):
        """
        This endpoint is used to delete the requested image under the user's folder.
        It uses the JWT to retrieve user information.
        """
        user_id = get_jwt_identity()
        folder = f"user_{user_id}"

        # check if filename is URL secure
        if not image_helper.is_filename_safe(filename):
            return {"message": gettext("image_illegal_file_name").format(filename)}, 400

        try:
            os.remove(image_helper.get_path(filename, folder=folder))
            return {"message": gettext("image_deleted").format(filename)}, 200
        except FileNotFoundError:
            return {"message": gettext("image_not_found").format(filename)}, 404
        except:
            traceback.print_exc()
            return {"message": gettext("image_delete_failed")}, 500


class AvatarUpload(Resource):
    @jwt_required
    def put(self):
        """
        This endpoint is used to upload user avatar. All avatars are named after the user's id
        in such format: user_{id}.{ext}.
        It will overwrite the existing avatar.
        """
        data = image_schema.load(request.files)
        filename = f"user_{get_jwt_identity()}"
        folder = "avatars"
        avatar_path = image_helper.find_image_any_format(filename, folder)
        if avatar_path:
            try:
                os.remove(avatar_path)
            except:
                return {"message": gettext("avatar_delete_failed")}, 500

        try:
            ext = image_helper.get_extension(data["image"].filename)
            avatar = filename + ext  # use our naming format + true extension
            avatar_path = image_helper.save_image(
                data["image"], folder=folder, name=avatar
            )
            basename = image_helper.get_basename(avatar_path)
            return {"message": gettext("avatar_uploaded").format(basename)}, 200
        except UploadNotAllowed:  # forbidden file type
            extension = image_helper.get_extension(data["image"])
            return {"message": gettext("image_illegal_extension").format(extension)}, 400


class Avatar(Resource):
    @classmethod
    def get(cls, user_id: int):
        """
        This endpoint returns the avatar of the user specified by user_id.
        """
        folder = "avatars"
        filename = f"user_{user_id}"
        avatar = image_helper.find_image_any_format(filename, folder)
        if avatar:
            return send_file(avatar)
        return {"message": gettext("avatar_not_found")}, 404
