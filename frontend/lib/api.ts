const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

async function request<T>(path: string, body?: unknown): Promise<T> {
  let res: Response;
  try {
    res = await fetch(`${API_URL}${path}`, {
      method: body ? "POST" : "GET",
      headers: { "Content-Type": "application/json" },
      body: body ? JSON.stringify(body) : undefined,
    });
  } catch {
    throw new Error("Impossible de joindre le serveur. Vérifiez votre connexion.");
  }

  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error((data as { detail?: string }).detail ?? "Une erreur est survenue.");
  return data as T;
}

export const login = (email: string, password: string) =>
  request<{ access_token: string }>("/auth/login", { email, password });

export const signup = (payload: {
  nom: string;
  prenom: string;
  email: string;
  password: string;
  telephone?: string;
  hopital?: string;
}) => request<{ user: string; medecin_id: number; need_email_confirmation: boolean }>("/auth/signup", payload);

export const forgotPassword = (email: string) =>
  request<{ message: string }>("/auth/forgot-password", { email });

export const resetPassword = (access_token: string, refresh_token: string, new_password: string) =>
  request<{ message: string }>("/auth/reset-password", { access_token, refresh_token, new_password });