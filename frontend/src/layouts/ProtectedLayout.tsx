/* 
This layout is used to protect routes that require authentication.
It checks if the user is authenticated and then renders the children components.
If the user is not authenticated, it redirects them to the login page.
*/

// React
import { useEffect, useState } from "react";
import { useLocation, Navigate, Outlet } from "react-router-dom";

// Zustand
import { useUserStore } from "@/stores/UserStore";
import { useTenantStore } from "@/stores/TenantStore";

// API
import { authUserMeRetrieve } from "@/api/django/authentication-user/authentication-user";
import { tenantsTenantMeRetrieve } from "@/api/django/tenant-info/tenant-info";

const ProtectedLayout = () => {
  /* ---------------------------------- HOOKS --------------------------------- */
  const location = useLocation();
  const { setUser } = useUserStore();
  const { setTenant } = useTenantStore();

  // Local useStates
  const [isLoading, setIsLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Load the user
  useEffect(() => {
    const controller = new AbortController();

    const fetchUserData = async () => {
      setIsLoading(true);

      try {
        const userDetails = await authUserMeRetrieve({
          headers: {
            "Content-Type": "application/json"
          }
        });

        // Set the user details
        console.debug("User logged in:", userDetails);

        const tenantDetails = await tenantsTenantMeRetrieve({
          headers: {
            "Content-Type": "application/json"
          }
        });

        // Set the tenant details
        console.debug("Tenant details:", tenantDetails);

        // Set the user details
        setUser(userDetails);

        // Set the tenant details
        setTenant(tenantDetails);

        // Set the authenticated state
        setIsAuthenticated(true);
        setIsLoading(false);
      } catch {
        console.debug("User not logged in");
        setIsAuthenticated(false);
        setIsLoading(false);
      }
    };

    fetchUserData();

    return () => {
      // Cleanup
      controller.abort();
    };
  }, []);

  /* --------------------------------- RENDER --------------------------------- */
  if (isLoading) {
    return (
      <div className="flex h-full w-full items-center justify-center">
        Loading...
      </div>
    );
  }

  return isAuthenticated ? (
    <Outlet />
  ) : (
    // If a user is not authenticated, navigate them to the login page
    // Provide the state prop to navigate the user to what they were doing
    <Navigate to="/login" state={{ from: location }} replace />
  );
};

export default ProtectedLayout;
