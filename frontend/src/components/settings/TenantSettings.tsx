import { useState, useEffect } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage
} from "@/components/ui/form";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { toast } from "sonner";
import { useUserStore } from "@/stores/UserStore";
import {
  tenantsTenantMeRetrieve,
  tenantsTenantMeUpdate
} from "@/api/django/tenant-info/tenant-info";
import { TenantLogoUpload } from "./TenantLogoUpload";

/* ----------------------------------- Zod ---------------------------------- */
const TenantNameSchema = z.object({
  name: z
    .string()
    .min(1, "Team name is required")
    .max(100, "Team name must be 100 characters or less")
});

type TenantNameValues = z.infer<typeof TenantNameSchema>;

export function TenantSettings() {
  const { updateTenant } = useUserStore();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  const form = useForm<TenantNameValues>({
    resolver: zodResolver(TenantNameSchema),
    defaultValues: {
      name: ""
    }
  });

  // Fetch tenant data on mount
  useEffect(() => {
    const fetchTenant = async () => {
      try {
        const tenant = await tenantsTenantMeRetrieve();
        form.reset({
          name: tenant.name ?? ""
        });
      } catch (error) {
        console.error("Failed to fetch tenant data:", error);
        toast.error("Failed to load team information.");
      } finally {
        setIsLoading(false);
      }
    };
    fetchTenant();
  }, [form]);

  const onSubmit = async (values: TenantNameValues) => {
    setIsSubmitting(true);
    try {
      const updatedTenant = await tenantsTenantMeUpdate({
        name: values.name
      });

      // Update the user store with the new tenant data
      updateTenant({
        pk: updatedTenant.pk,
        name: updatedTenant.name,
        slug: updatedTenant.slug
      });

      toast.success("Team name updated successfully");
    } catch (error) {
      console.error("Failed to update team name:", error);
      toast.error("Failed to update team name. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Team Logo Card */}
      <Card className="max-w-lg">
        <CardHeader>
          <CardTitle>Team Logo</CardTitle>
          <CardDescription>Upload or update your team's logo.</CardDescription>
        </CardHeader>
        <CardContent>
          <TenantLogoUpload />
        </CardContent>
      </Card>

      {/* Team Name Card */}
      <Card className="max-w-lg">
        <CardHeader>
          <CardTitle>Team Information</CardTitle>
          <CardDescription>Update your team's name.</CardDescription>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="space-y-4">
              <div className="space-y-2">
                <div className="h-4 w-20 animate-pulse rounded bg-muted" />
                <div className="h-10 w-full animate-pulse rounded bg-muted" />
              </div>
              <div className="h-10 w-28 animate-pulse rounded bg-muted" />
            </div>
          ) : (
            <Form {...form}>
              <form
                onSubmit={form.handleSubmit(onSubmit)}
                className="space-y-4"
              >
                <FormField
                  control={form.control}
                  name="name"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Team Name</FormLabel>
                      <FormControl>
                        <Input placeholder="My Team" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <Button
                  type="submit"
                  className="hover:cursor-pointer"
                  loading={isSubmitting}
                >
                  Save Changes
                </Button>
              </form>
            </Form>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
