import { useState, useEffect } from "react";
import SideBarLayout from "@/layouts/SideBarLayout";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
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
import { authUserMePartialUpdate } from "@/api/django/auth/auth";
import { AvatarUpload } from "@/components/settings/AvatarUpload";

/* ----------------------------------- Zod ---------------------------------- */
const UserProfileSchema = z.object({
  first_name: z.string().max(30, "First name must be 30 characters or less"),
  last_name: z.string().max(30, "Last name must be 30 characters or less")
});

type UserProfileValues = z.infer<typeof UserProfileSchema>;

const Settings = () => {
  const { user, setUser } = useUserStore();
  const [isSubmitting, setIsSubmitting] = useState(false);

  const form = useForm<UserProfileValues>({
    resolver: zodResolver(UserProfileSchema),
    defaultValues: {
      first_name: "",
      last_name: ""
    }
  });

  // Update form when user data loads
  useEffect(() => {
    if (user) {
      form.reset({
        first_name: user.first_name ?? "",
        last_name: user.last_name ?? ""
      });
    }
  }, [user, form]);

  const onSubmit = async (values: UserProfileValues) => {
    setIsSubmitting(true);
    try {
      const updatedUser = await authUserMePartialUpdate({
        first_name: values.first_name,
        last_name: values.last_name
      });

      // Update the user store with the new data
      setUser({
        ...user!,
        first_name: updatedUser.first_name,
        last_name: updatedUser.last_name
      });

      toast.success("Profile updated successfully");
    } catch (error) {
      console.error("Failed to update profile:", error);
      toast.error("Failed to update profile. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <SideBarLayout title="Settings">
      <div className="flex w-full justify-center">
        <div id="settings-container" className="flex flex-col gap-6">
          <Tabs defaultValue="user" className="w-full">
            <TabsList className="grid w-full max-w-md grid-cols-2">
              <TabsTrigger value="user">User Settings</TabsTrigger>
              <TabsTrigger value="team">Team Settings</TabsTrigger>
            </TabsList>
            <TabsContent value="user" className="mt-6 space-y-6">
              {/* Profile Picture Card */}
              <Card className="max-w-lg">
                <CardHeader>
                  <CardTitle>Profile Picture</CardTitle>
                  <CardDescription>
                    Upload or update your profile picture.
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <AvatarUpload />
                </CardContent>
              </Card>

              {/* Profile Information Card */}
              <Card className="max-w-lg">
                <CardHeader>
                  <CardTitle>Profile Information</CardTitle>
                  <CardDescription>
                    Update your personal information.
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <Form {...form}>
                    <form
                      onSubmit={form.handleSubmit(onSubmit)}
                      className="space-y-4"
                    >
                      <FormField
                        control={form.control}
                        name="first_name"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel>First Name</FormLabel>
                            <FormControl>
                              <Input placeholder="John" {...field} />
                            </FormControl>
                            <FormMessage />
                          </FormItem>
                        )}
                      />

                      <FormField
                        control={form.control}
                        name="last_name"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel>Last Name</FormLabel>
                            <FormControl>
                              <Input placeholder="Doe" {...field} />
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
                </CardContent>
              </Card>
            </TabsContent>
            <TabsContent value="team" className="mt-6">
              <div className="space-y-4">
                <h2 className="text-lg font-semibold">Team Settings</h2>
                <p className="text-muted-foreground">
                  Manage your team settings and member permissions.
                </p>
              </div>
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </SideBarLayout>
  );
};

export default Settings;
