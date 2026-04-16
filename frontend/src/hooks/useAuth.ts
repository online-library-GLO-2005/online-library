import {
  loginRequest,
  logoutRequest,
  signupRequest,
} from '../services/authService';
import { useAuthStore } from '../store/authStore';
import type { LoginData, LoginResponse, SignupData } from '../types/auth';
import type { User } from '../types/user';
import { showError } from '../utils/getErrorMessage';
import { toast } from 'react-hot-toast';
import { useNavigate } from 'react-router-dom';

export const useAuth = () => {
  const { setToken, setUser, logout: clearAuth } = useAuthStore();
  const navigate = useNavigate();
  const authenticate = async (data: LoginResponse | undefined) => {
    if (!data) {
      throw new Error('Missing login response data');
    }

    setToken(data.token_access);
    setUser(data.user as User);
    toast.success(`Welcome ${data.user.name}`);
    navigate('/');
  };

  const login = async (email: string, password: string) => {
    const loginData: LoginData = { email, password };

    try {
      const res = await loginRequest(loginData);
      authenticate(res);
    } catch (error) {
      showError(error);
    }
  };

  const signup = async (name: string, email: string, password: string) => {
    const signupData: SignupData = { name, email, password };

    try {
      const res = await signupRequest(signupData);
      authenticate(res);
    } catch (error) {
      showError(error);
    }
  };

  const logout = async () => {
    try {
      await logoutRequest();
      toast.success(`Goodbye!`);
    } catch (error) {
      showError(error);
    }
    clearAuth();
  };

  return { login, signup, logout };
};
