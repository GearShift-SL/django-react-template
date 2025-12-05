import { LoginForm } from "@/components/login/LoginForm";
import type { LoginFormValues } from "@/components/login/LoginForm";
import { toast } from "sonner";
import RedirectIfAuthenticatedLayout from "@/layouts/RedirectIfAuthenticatedLayout";
import { authStart } from "@/api/django/auth/auth";
import { useState } from "react";
import {
  InputOTP,
  InputOTPGroup,
  InputOTPSeparator,
  InputOTPSlot
} from "@/components/ui/input-otp";
import { authConfirmCode } from "@/api/django/auth/auth";
import { useNavigate } from "react-router-dom";
import Icon from "@/assets/icon.svg?react";
import {
  GoogleOAuthProvider,
  GoogleLogin,
  type CredentialResponse
} from "@react-oauth/google";
import { authProviderToken } from "@/api/django/auth/auth";

const Login = () => {
  const navigate = useNavigate();

  const [step, setStep] = useState<"initial" | "code-login" | "google-login">(
    "initial"
  );
  const [isLoading, setIsLoading] = useState(false);

  const handleEmailLogin = async (formData: LoginFormValues) => {
    console.debug("Email login:", formData);

    try {
      setIsLoading(true);
      await authStart("browser", {
        email: formData.email
      });
      setIsLoading(false);
    } catch (error: any) {
      // 401 means the code was sent successfully
      if (error?.response?.status === 401) {
        console.debug("Code sent successfully");
        setStep("code-login");
        return;
      }

      // Handle other errors
      console.error(error);
      toast.error("Something went wrong. Please try again later.");
    }
  };

  const handleCodeLogin = async (code: string) => {
    try {
      setIsLoading(true);
      await authConfirmCode("browser", {
        code: code
      });
      console.log("Logged in with code");

      // Navigate to the home page
      navigate("/");
      setIsLoading(false);
    } catch (error: any) {
      console.error("Error logging in with code", error);
    }
  };

  const handleGoogleLogin = async (credentialResponse: CredentialResponse) => {
    if (!credentialResponse.credential) {
      console.error("No credential found");
      return;
    }

    // Send the credential to the allauth api provider token endpoint
    try {
      setIsLoading(true);
      await authProviderToken("browser", {
        provider: "google",
        process: "login",
        token: {
          client_id: credentialResponse.clientId ?? "",
          id_token: credentialResponse.credential
        }
      });

      console.debug("Logged in with Google");

      // Navigate to the home page
      navigate("/");
      setIsLoading(false);
    } catch (error: any) {
      console.error("Error logging in with Google", error);
    }
  };

  return (
    <RedirectIfAuthenticatedLayout>
      <div className="bg-background flex min-h-svh flex-col items-center justify-center gap-6 p-6 md:p-10">
        <div className="w-full max-w-sm">
          <div className={"flex flex-col gap-6"}>
            {/* Header */}
            <div className="flex flex-col items-center gap-2">
              <a
                href="#"
                className="flex flex-col items-center gap-2 font-medium"
              >
                <span className="sr-only">AutoIPC</span>
              </a>
              <Icon className="h-[50px]" />
              <h1 className="text-xl font-bold">Welcome to React Frontend</h1>
            </div>
            {step === "initial" && (
              <>
                {/* Login form */}
                <LoginForm
                  onSubmit={handleEmailLogin}
                  isSubmitting={isLoading}
                />

                {/* Google Sign In */}
                <div className="after:border-border relative text-center text-sm after:absolute after:inset-0 after:top-1/2 after:z-0 after:flex after:items-center after:border-t">
                  <span className="bg-background text-muted-foreground relative z-10 px-2">
                    or
                  </span>
                </div>
                <GoogleOAuthProvider clientId="370259082711-8t6vtage248pl6vjaulcom3nve1qes1r.apps.googleusercontent.com">
                  <div className="flex justify-center w-full">
                    <GoogleLogin
                      onSuccess={handleGoogleLogin}
                      onError={() => console.log("Google Login Failed")}
                      // useOneTap // Optional: show auto-login prompt
                      theme="outline"
                      type="standard"
                      shape="circle"
                      text="signin_with"
                      size="large"
                    />
                  </div>
                </GoogleOAuthProvider>
              </>
            )}

            {step === "code-login" && (
              <>
                <div className="text-muted-foreground text-center text-sm">
                  We have sent you a code to your email. Please enter it below.
                  abajo.
                </div>
                <div className="flex w-full justify-center">
                  <InputOTP maxLength={6} onComplete={handleCodeLogin}>
                    <InputOTPGroup>
                      <InputOTPSlot index={0} />
                      <InputOTPSlot index={1} />
                      <InputOTPSlot index={2} />
                    </InputOTPGroup>
                    <InputOTPSeparator />
                    <InputOTPGroup>
                      <InputOTPSlot index={3} />
                      <InputOTPSlot index={4} />
                      <InputOTPSlot index={5} />
                    </InputOTPGroup>
                  </InputOTP>
                </div>
              </>
            )}

            {/* Login/Signup footer */}
            <div className="text-muted-foreground *:[a]:hover:text-primary text-center text-xs text-balance *:[a]:underline *:[a]:underline-offset-4">
              If you already have an account, we will log you in automatically.
            </div>

            {/* Terms of Service and Privacy Policy */}
            <div className="text-muted-foreground *:[a]:hover:text-primary text-center text-xs text-balance *:[a]:underline *:[a]:underline-offset-4">
              By continuing, you agree to our{" "}
              <a href="https://mydomain.com/terms/" target="_blank">
                Terms of Service
              </a>{" "}
              and{" "}
              <a href="https://mydomain.com/privacy/" target="_blank">
                Privacy Policy
              </a>
              .
            </div>
          </div>
        </div>
      </div>
    </RedirectIfAuthenticatedLayout>
  );
};

export default Login;
