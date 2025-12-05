import { useState, useRef } from "react";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { customAxios } from "@/api/axios";
import { Camera, Trash2 } from "lucide-react";
import { toast } from "sonner";
import { useUserStore } from "@/stores/UserStore";

export function AvatarUpload() {
  const { user, setUser } = useUserStore();
  const [isUploading, setIsUploading] = useState(false);
  const [preview, setPreview] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      // Validate file type
      if (!file.type.startsWith("image/")) {
        toast.error("Please select an image file");
        return;
      }
      // Validate file size (max 5MB)
      if (file.size > 5 * 1024 * 1024) {
        toast.error("Image must be smaller than 5MB");
        return;
      }
      // Create preview
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleUpload = async () => {
    const file = fileInputRef.current?.files?.[0];
    if (!file) return;

    setIsUploading(true);
    try {
      const formData = new FormData();
      formData.append("avatar", file);

      const response = await customAxios.patch("/auth/user/me/profile/", formData, {
        headers: {
          "Content-Type": "multipart/form-data"
        }
      });

      // Update the user store with the new avatar
      setUser({
        ...user!,
        profile: {
          ...user!.profile,
          avatar: response.data.avatar
        }
      });

      setPreview(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
      toast.success("Profile picture updated successfully");
    } catch (error) {
      console.error("Failed to upload profile picture:", error);
      toast.error("Failed to upload profile picture. Please try again.");
    } finally {
      setIsUploading(false);
    }
  };

  const handleDelete = async () => {
    setIsUploading(true);
    try {
      const formData = new FormData();
      formData.append("avatar", "");

      await customAxios.patch("/auth/user/me/profile/", formData, {
        headers: {
          "Content-Type": "multipart/form-data"
        }
      });

      // Update the user store to remove the avatar
      setUser({
        ...user!,
        profile: {
          ...user!.profile,
          avatar: null
        }
      });

      setPreview(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
      toast.success("Profile picture removed");
    } catch (error) {
      console.error("Failed to remove profile picture:", error);
      toast.error("Failed to remove profile picture. Please try again.");
    } finally {
      setIsUploading(false);
    }
  };

  const cancelPreview = () => {
    setPreview(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  return (
    <div className="flex flex-col items-center gap-6 sm:flex-row sm:items-start">
      {/* Avatar Preview */}
      <div className="relative group">
        <Avatar className="h-24 w-24">
          <AvatarImage
            src={preview ?? user?.profile.avatar ?? undefined}
            alt={user?.full_name}
          />
          <AvatarFallback className="text-2xl">
            {user?.first_name?.charAt(0) ?? "?"}
            {user?.last_name?.charAt(0) ?? ""}
          </AvatarFallback>
        </Avatar>
        {!preview && (
          <button
            type="button"
            onClick={() => fileInputRef.current?.click()}
            className="absolute inset-0 flex items-center justify-center rounded-full bg-black/50 opacity-0 transition-opacity group-hover:opacity-100 hover:cursor-pointer"
            disabled={isUploading}
          >
            <Camera className="h-6 w-6 text-white" />
          </button>
        )}
      </div>

      {/* Upload Controls */}
      <div className="flex flex-1 flex-col gap-3">
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          onChange={handleFileSelect}
          className="hidden"
        />

        {preview ? (
          // Show save/cancel when there's a preview
          <div className="flex gap-2">
            <Button
              type="button"
              onClick={handleUpload}
              loading={isUploading}
              className="hover:cursor-pointer"
            >
              Save Picture
            </Button>
            <Button
              type="button"
              variant="outline"
              onClick={cancelPreview}
              disabled={isUploading}
              className="hover:cursor-pointer"
            >
              Cancel
            </Button>
          </div>
        ) : (
          // Show upload/remove buttons
          <div className="flex gap-2">
            <Button
              type="button"
              variant="outline"
              onClick={() => fileInputRef.current?.click()}
              disabled={isUploading}
              className="hover:cursor-pointer"
            >
              <Camera className="mr-2 h-4 w-4" />
              Upload New
            </Button>
            {user?.profile.avatar && (
              <Button
                type="button"
                variant="outline"
                onClick={handleDelete}
                loading={isUploading}
                className="text-destructive hover:text-destructive hover:cursor-pointer"
              >
                <Trash2 className="mr-2 h-4 w-4" />
                Remove
              </Button>
            )}
          </div>
        )}

        <p className="text-sm text-muted-foreground">
          JPG, PNG or GIF. Max size 5MB.
        </p>
      </div>
    </div>
  );
}

