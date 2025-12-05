import SideBarLayout from "@/layouts/SideBarLayout";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

const Settings = () => {
  return (
    <SideBarLayout title="Settings">
      <div className="flex flex-col gap-6">
        <Tabs defaultValue="user" className="w-full">
          <TabsList className="grid w-full max-w-md grid-cols-2">
            <TabsTrigger value="user">User Settings</TabsTrigger>
            <TabsTrigger value="team">Team Settings</TabsTrigger>
          </TabsList>
          <TabsContent value="user" className="mt-6">
            <div className="space-y-4">
              <h2 className="text-lg font-semibold">User Settings</h2>
              <p className="text-muted-foreground">
                Manage your personal account settings and preferences.
              </p>
            </div>
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
    </SideBarLayout>
  );
};

export default Settings;
