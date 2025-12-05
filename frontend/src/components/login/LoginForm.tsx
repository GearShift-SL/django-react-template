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

// Form imports
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";

/* ----------------------------------- Zod ---------------------------------- */
export const LoginFormSchema = z.object({
  email: z.email("Please enter a valid email")
});

export type LoginFormValues = z.infer<typeof LoginFormSchema>;

/* -------------------------------- Interface ------------------------------- */
interface Props {
  onSubmit: (values: LoginFormValues) => void;
  isSubmitting?: boolean;
}

export function LoginForm({ onSubmit, isSubmitting }: Props) {
  /* ----------------------------- React hook form ---------------------------- */
  const form = useForm<z.infer<typeof LoginFormSchema>>({
    resolver: zodResolver(LoginFormSchema),
    defaultValues: {
      email: ""
    }
  });

  /* --------------------------------- Render --------------------------------- */
  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input placeholder="ejemplo@correo.com" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <Button type="submit" className="w-full" loading={isSubmitting}>
          Continuar con email
        </Button>
      </form>
    </Form>
  );
}
