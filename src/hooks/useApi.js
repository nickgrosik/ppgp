import { useState } from "react";
import toast from "react-hot-toast";

export function useApi(options = {}) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);
  const [message, setMessage] = useState("");

  async function run(operation, messages = {}) {
    setLoading(true);
    setError(null);

    try {
      const data = await operation();
      const successMessage = messages.successMessage || "Done. The machine remains obedient.";
      const successToast = messages.successToast || "Done. Try not to act surprised.";
      setResult(data);
      setMessage(successMessage);
      toast.success(successToast);
      options.onSuccess?.(data, successMessage);
      return data;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Something broke. You probably touched it.";
      const narratorMessage = messages.errorMessage || "Something broke. You probably touched it.";
      const errorToast = messages.errorToast || "Nope. Try again with fewer mistakes.";
      setError(errorMessage);
      setMessage(narratorMessage);
      toast.error(errorToast);
      options.onError?.(err, narratorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  }

  return { run, loading, error, result, message };
}
