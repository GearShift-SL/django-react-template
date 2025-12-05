import { create } from "zustand";

interface User {
  pk: number;
  email: string;
  first_name?: string;
  last_name?: string;
  full_name?: string;
  avatar?: string;
}

interface UserStore {
  user: User | undefined;
  setUser: (user: User) => void;
  clearUser: () => void;
}

export const useUserStore = create<UserStore>((set) => ({
  user: undefined,
  setUser: (user) =>
    set({
      user: {
        ...user,
        full_name:
          user.full_name ??
          ([user.first_name, user.last_name].filter(Boolean).join(" ").trim() ||
            undefined)
      }
    }),
  clearUser: () => set({ user: undefined })
}));
