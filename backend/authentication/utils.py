from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


def avatar_upload_path(instance, filename):
    """
    Generate upload path for avatar images.
    Format: avatars/<user_pk>_avatar.webp

    Args:
        instance: UserProfile instance
        filename: Original filename (will be replaced)

    Returns:
        str: Upload path
    """
    user_pk = instance.user.pk
    return f"avatars/{user_pk}_avatar.webp"


def process_avatar_image(image_field, user_pk):
    """
    Process an uploaded avatar image:
    - Convert to WebP format
    - Resize to max 300x300px while maintaining aspect ratio
    - Compress for optimal file size
    - Rename to <user_pk>_avatar.webp

    Args:
        image_field: Django ImageField or uploaded file
        user_pk: Primary key of the user

    Returns:
        InMemoryUploadedFile: Processed image ready to be saved
    """
    if not image_field:
        return None

    # Open the image
    img = Image.open(image_field)

    # Convert RGBA to RGB if necessary (WebP supports RGBA but better compatibility with RGB)
    if img.mode in ("RGBA", "LA", "P"):
        # Create a white background
        background = Image.new("RGB", img.size, (255, 255, 255))
        if img.mode == "P":
            img = img.convert("RGBA")
        background.paste(
            img, mask=img.split()[-1] if img.mode in ("RGBA", "LA") else None
        )
        img = background
    elif img.mode != "RGB":
        img = img.convert("RGB")

    # Calculate new dimensions maintaining aspect ratio
    # The longer side should be max 300px
    max_size = 300
    width, height = img.size

    if width > max_size or height > max_size:
        if width > height:
            new_width = max_size
            new_height = int((max_size / width) * height)
        else:
            new_height = max_size
            new_width = int((max_size / height) * width)

        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Save to BytesIO as WebP
    output = BytesIO()
    img.save(output, format="WEBP", quality=85, method=6)
    output.seek(0)

    # Use user pk for filename
    new_filename = f"{user_pk}_avatar.webp"

    # Create a new InMemoryUploadedFile
    return InMemoryUploadedFile(
        output, "ImageField", new_filename, "image/webp", sys.getsizeof(output), None
    )
