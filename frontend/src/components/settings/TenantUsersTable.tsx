import { useState, useEffect } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow
} from "@/components/ui/table";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle
} from "@/components/ui/dialog";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue
} from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger
} from "@/components/ui/tooltip";
import { Pencil, Plus } from "lucide-react";
import { toast } from "sonner";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  tenantsTenantUsersList,
  tenantsTenantUsersUpdate
} from "@/api/django/tenant-users/tenant-users";
import {
  tenantsInvitationsCreate,
  tenantsInvitationsList
} from "@/api/django/tenant-invitations/tenant-invitations";
import type {
  TenantUserList,
  Invitation
} from "@/api/django/djangoAPI.schemas";
import { RoleEnum } from "@/api/django/djangoAPI.schemas";
import { useTenantStore } from "@/stores/TenantStore";

const roleLabels: Record<string, string> = {
  owner: "Owner",
  admin: "Admin",
  user: "User"
};

const roleBadgeVariants: Record<string, "default" | "secondary" | "outline"> = {
  owner: "default",
  admin: "secondary",
  user: "outline"
};

// Combined type for displaying both users and pending invitations
type UserOrInvitation =
  | { type: "user"; data: TenantUserList }
  | { type: "invitation"; data: Invitation };

export function TenantUsersTable() {
  const { tenant } = useTenantStore();
  const [users, setUsers] = useState<TenantUserList[]>([]);
  const [invitations, setInvitations] = useState<Invitation[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [editingUser, setEditingUser] = useState<TenantUserList | null>(null);
  const [selectedRole, setSelectedRole] = useState<string>("");
  const [isUpdating, setIsUpdating] = useState(false);
  const [isInviteDialogOpen, setIsInviteDialogOpen] = useState(false);
  const [inviteEmail, setInviteEmail] = useState("");
  const [isSendingInvite, setIsSendingInvite] = useState(false);

  const fetchUsers = async () => {
    try {
      const [usersData, invitationsData] = await Promise.all([
        tenantsTenantUsersList(),
        tenantsInvitationsList()
      ]);
      setUsers(usersData);
      // Only show pending invitations (not yet accepted)
      setInvitations(invitationsData.filter((inv) => inv.accepted_at === null));
    } catch (error) {
      console.error("Failed to fetch tenant users:", error);
      toast.error("Failed to load team members.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleEditRole = (user: TenantUserList) => {
    setEditingUser(user);
    setSelectedRole(user.role);
  };

  const handleCloseDialog = () => {
    setEditingUser(null);
    setSelectedRole("");
  };

  const handleUpdateRole = async () => {
    if (!editingUser || !selectedRole) return;

    setIsUpdating(true);
    try {
      await tenantsTenantUsersUpdate(editingUser.pk, {
        role: selectedRole as (typeof RoleEnum)[keyof typeof RoleEnum]
      });

      // Update local state
      setUsers((prevUsers) =>
        prevUsers.map((user) =>
          user.pk === editingUser.pk
            ? {
                ...user,
                role: selectedRole as (typeof RoleEnum)[keyof typeof RoleEnum]
              }
            : user
        )
      );

      toast.success("Role updated successfully");
      handleCloseDialog();
    } catch (error) {
      console.error("Failed to update role:", error);
      toast.error("Failed to update role. Please try again.");
    } finally {
      setIsUpdating(false);
    }
  };

  const handleOpenInviteDialog = () => {
    setIsInviteDialogOpen(true);
    setInviteEmail("");
  };

  const handleCloseInviteDialog = () => {
    setIsInviteDialogOpen(false);
    setInviteEmail("");
  };

  const handleSendInvite = async () => {
    if (!inviteEmail.trim()) {
      toast.error("Please enter an email address");
      return;
    }

    // Basic email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(inviteEmail)) {
      toast.error("Please enter a valid email address");
      return;
    }

    setIsSendingInvite(true);
    try {
      await tenantsInvitationsCreate({ email: inviteEmail });
      toast.success("Invitation sent successfully");
      handleCloseInviteDialog();
      // Optionally refresh the users list
      fetchUsers();
    } catch (error) {
      console.error("Failed to send invitation:", error);
      toast.error("Failed to send invitation. Please try again.");
    } finally {
      setIsSendingInvite(false);
    }
  };

  const getUserName = (user: TenantUserList) => {
    const fullName = `${user.first_name} ${user.last_name}`.trim();
    return fullName || "—";
  };

  const getUserNameOrEmail = (user: TenantUserList) => {
    const fullName = `${user.first_name} ${user.last_name}`.trim();
    return fullName || user.email || "—";
  };

  // Combine users and pending invitations for display
  const combinedList: UserOrInvitation[] = [
    ...users.map((user) => ({ type: "user" as const, data: user })),
    ...invitations.map((invitation) => ({
      type: "invitation" as const,
      data: invitation
    }))
  ];

  return (
    <>
      <Card>
        <CardHeader>
          <CardTitle>Team Members</CardTitle>
          <CardDescription>
            Manage your team members and their roles.
          </CardDescription>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="space-y-3">
              {[...Array(3)].map((_, i) => (
                <div key={i} className="flex items-center gap-4">
                  <div className="h-4 w-32 animate-pulse rounded bg-muted" />
                  <div className="h-4 w-48 animate-pulse rounded bg-muted" />
                  <div className="h-4 w-16 animate-pulse rounded bg-muted" />
                  <div className="h-8 w-8 animate-pulse rounded bg-muted" />
                </div>
              ))}
            </div>
          ) : combinedList.length === 0 ? (
            <p className="text-sm text-muted-foreground">
              No team members found.
            </p>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Name</TableHead>
                  <TableHead>Email</TableHead>
                  <TableHead>Role</TableHead>
                  <TableHead className="w-[70px]"></TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {combinedList.map((item, index) => {
                  if (item.type === "user") {
                    const user = item.data;
                    return (
                      <TableRow key={`user-${user.pk}`}>
                        <TableCell className="font-medium">
                          {getUserName(user)}
                        </TableCell>
                        <TableCell>{user.email}</TableCell>
                        <TableCell>
                          <Badge
                            variant={roleBadgeVariants[user.role] || "outline"}
                          >
                            {roleLabels[user.role] || user.role}
                          </Badge>
                        </TableCell>
                        <TableCell>
                          {user.role === "owner" ? (
                            <Tooltip>
                              <TooltipTrigger asChild>
                                <span className="inline-block">
                                  <Button
                                    variant="ghost"
                                    size="sm"
                                    disabled
                                    className="h-8 w-8 p-0"
                                  >
                                    <Pencil className="h-4 w-4" />
                                    <span className="sr-only">Edit role</span>
                                  </Button>
                                </span>
                              </TooltipTrigger>
                              <TooltipContent
                                side="left"
                                className="max-w-[200px]"
                              >
                                {tenant?.me?.role === RoleEnum.owner
                                  ? `To modify or delete this user, transfer ownership to another
                                user first`
                                  : `You cannot edit the role of the owner`}
                              </TooltipContent>
                            </Tooltip>
                          ) : (
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => handleEditRole(user)}
                              className="h-8 w-8 p-0"
                            >
                              <Pencil className="h-4 w-4" />
                              <span className="sr-only">Edit role</span>
                            </Button>
                          )}
                        </TableCell>
                      </TableRow>
                    );
                  } else {
                    const invitation = item.data;
                    return (
                      <TableRow key={`invitation-${invitation.email}-${index}`}>
                        <TableCell className="font-medium text-muted-foreground">
                          —
                        </TableCell>
                        <TableCell className="text-muted-foreground">
                          {invitation.email}
                        </TableCell>
                        <TableCell>
                          <Badge
                            variant="outline"
                            className="text-muted-foreground"
                          >
                            Pending
                          </Badge>
                        </TableCell>
                        <TableCell>
                          <Tooltip>
                            <TooltipTrigger asChild>
                              <span className="inline-block">
                                <Button
                                  variant="ghost"
                                  size="sm"
                                  disabled
                                  className="h-8 w-8 p-0"
                                >
                                  <Pencil className="h-4 w-4" />
                                  <span className="sr-only">Edit role</span>
                                </Button>
                              </span>
                            </TooltipTrigger>
                            <TooltipContent
                              side="left"
                              className="max-w-[200px]"
                            >
                              Cannot edit pending invitations
                            </TooltipContent>
                          </Tooltip>
                        </TableCell>
                      </TableRow>
                    );
                  }
                })}
              </TableBody>
            </Table>
          )}
          <div className="mt-4 flex justify-end">
            <Button
              variant="outline"
              size="sm"
              onClick={handleOpenInviteDialog}
              className="gap-2 hover:cursor-pointer"
            >
              <Plus className="h-4 w-4" />
              Invite User
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Edit Role Dialog */}
      <Dialog
        open={!!editingUser}
        onOpenChange={(open) => !open && handleCloseDialog()}
      >
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Edit Role</DialogTitle>
            <DialogDescription>
              Change the role for{" "}
              {editingUser ? getUserNameOrEmail(editingUser) : ""}.
            </DialogDescription>
          </DialogHeader>
          <div className="py-4">
            <Select value={selectedRole} onValueChange={setSelectedRole}>
              <SelectTrigger className="w-full">
                <SelectValue placeholder="Select a role" />
              </SelectTrigger>
              <SelectContent>
                {tenant?.me?.role === RoleEnum.owner && (
                  <SelectItem value={RoleEnum.owner}>Owner</SelectItem>
                )}
                <SelectItem value={RoleEnum.admin}>Admin</SelectItem>
                <SelectItem value={RoleEnum.user}>User</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={handleCloseDialog}>
              Cancel
            </Button>
            <Button
              onClick={handleUpdateRole}
              loading={isUpdating}
              disabled={selectedRole === editingUser?.role}
            >
              Save Changes
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Invite User Dialog */}
      <Dialog
        open={isInviteDialogOpen}
        onOpenChange={(open) => !open && handleCloseInviteDialog()}
      >
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Invite User</DialogTitle>
            <DialogDescription>
              Send an invitation to join your team. They will receive an email
              with instructions to create an account.
            </DialogDescription>
          </DialogHeader>
          <div className="py-4">
            <Label htmlFor="invite-email">Email</Label>
            <Input
              id="invite-email"
              type="email"
              placeholder="user@example.com"
              value={inviteEmail}
              onChange={(e) => setInviteEmail(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  handleSendInvite();
                }
              }}
              className="mt-2"
            />
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={handleCloseInviteDialog}>
              Cancel
            </Button>
            <Button onClick={handleSendInvite} loading={isSendingInvite}>
              Send Invitation
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  );
}
