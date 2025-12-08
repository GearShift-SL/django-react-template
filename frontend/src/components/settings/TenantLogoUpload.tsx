import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Camera, Trash2, ImageIcon } from "lucide-react";
import { toast } from "sonner";
import {
  tenantsTenantLogoRetrieve,
  tenantsTenantLogoCreate,
  tenantsTenantLogoDestroy,
  tenantsTenantMeRetrieve
} from "@/api/django/tenants/tenants";

export function TenantLogoUpload() {
  const [isUploading, setIsUploading] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [logoUrl, setLogoUrl] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Fetch current logo on mount
  useEffect(() => {
    const fetchLogo = async () => {
      try {
        const response = await tenantsTenantMeRetrieve();

        console.debug(response);

        setLogoUrl(response.logo || null);
      } catch {
        // Logo might not exist yet, which is fine
        setLogoUrl(null);
      } finally {
        setIsLoading(false);
      }
    };
    fetchLogo();
  }, []);

  const handleFileSelect = async (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0];
    if (!file) return;

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

    setIsUploading(true);
    try {
      const response = await tenantsTenantLogoCreate({ image: file });
      setLogoUrl(response.image);
      toast.success("Team logo updated successfully");
    } catch (error) {
      console.error("Failed to upload team logo:", error);
      toast.error("Failed to upload team logo. Please try again.");
    } finally {
      setIsUploading(false);
      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
    }
  };

  const handleDelete = async () => {
    setIsUploading(true);
    try {
      await tenantsTenantLogoDestroy();
      setLogoUrl(null);
      toast.success("Team logo removed");
    } catch (error) {
      console.error("Failed to remove team logo:", error);
      toast.error("Failed to remove team logo. Please try again.");
    } finally {
      setIsUploading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="flex flex-col gap-4">
        <div className="h-32 w-full max-w-xs animate-pulse rounded-lg bg-muted" />
        <div className="flex gap-2">
          <div className="h-10 w-32 animate-pulse rounded bg-muted" />
        </div>
        <div className="h-4 w-48 animate-pulse rounded bg-muted" />
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-4">
      {/* Logo Preview - Full Image Display */}
      {logoUrl ? (
        <div className="relative w-fit">
          <img
            src={logoUrl}
            alt="Team logo"
            className="max-h-32 max-w-xs rounded-lg border object-contain"
          />
        </div>
      ) : (
        <div className="flex h-32 w-full max-w-xs items-center justify-center rounded-lg border border-dashed bg-muted/50">
          <div className="flex flex-col items-center gap-2 text-muted-foreground">
            <ImageIcon className="h-10 w-10" />
            <span className="text-sm">No logo uploaded</span>
          </div>
        </div>
      )}

      {/* Upload Controls */}
      <div className="flex flex-col gap-3">
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          onChange={handleFileSelect}
          className="hidden"
        />

        <div className="flex gap-2">
          <Button
            type="button"
            variant="outline"
            onClick={() => fileInputRef.current?.click()}
            loading={isUploading}
            className="hover:cursor-pointer"
          >
            <Camera className="mr-2 h-4 w-4" />
            {logoUrl ? "Change Logo" : "Upload Logo"}
          </Button>
          {logoUrl && (
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

        <p className="text-sm text-muted-foreground">
          JPG, PNG or GIF. Max size 5MB.
        </p>
      </div>
    </div>
  );
}
