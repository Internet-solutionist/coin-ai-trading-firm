import numpy as np
import sympy as sp
from sympy import symbols, exp, log, diff, integrate, sqrt, pi
from typing import Dict, Tuple, Callable
import pandas as pd

# Symbolic variables for beautiful closed-form derivations
mu, sigma, theta, gamma, lam = symbols('mu sigma theta gamma lambda', real=True, positive=True)
x, t = symbols('x t', real=True)

class RenaissanceMath:
    """Elegant mathematical kernels for sovereign alpha generation."""

    @staticmethod
    def geometric_brownian_motion_with_mean_reversion(
        S0: float, mu: float, sigma: float, kappa: float, theta: float, T: float, steps: int = 1000
    ) -> np.ndarray:
        """Beautiful mean-reverting GBM (Ornstein-Uhlenbeck inspired)."""
        dt = T / steps
        S = np.zeros(steps)
        S[0] = S0
        for i in range(1, steps):
            dW = np.random.normal(0, np.sqrt(dt))
            S[i] = S[i-1] + kappa * (theta - S[i-1]) * dt + sigma * S[i-1] * dW
        return S

    @staticmethod
    def information_geometric_edge(
        p_regime: np.ndarray, q_regime: np.ndarray
    ) -> float:
        """Renaissance-style information geometry regime edge (KL divergence)."""
        p = np.clip(p_regime, 1e-10, 1)
        q = np.clip(q_regime, 1e-10, 1)
        return np.sum(p * np.log(p / q))

    @staticmethod
    def symbolic_kelly_fraction(
        edge: float, odds: float, bankroll_risk: float = 0.02
    ) -> sp.Expr:
        """Elegant symbolic Kelly criterion derivation."""
        b = symbols('b')  # odds
        p = symbols('p')  # win probability
        kelly = (b * p - (1 - p)) / b
        return kelly.subs({b: odds, p: (edge + 1) / 2})

    @staticmethod
    def closed_form_sharpe_surface(
        returns: np.ndarray, risk_free: float = 0.0
    ) -> Dict[str, float]:
        """Beautiful closed-form Sharpe surface statistics."""
        mu = np.mean(returns)
        sigma = np.std(returns, ddof=1)
        sharpe = (mu - risk_free) / sigma if sigma > 0 else 0.0
        return {
            "mu": mu,
            "sigma": sigma,
            "sharpe": sharpe,
            "information_ratio": mu / sigma if sigma > 0 else 0.0
        }

    @staticmethod
    def kernel_ridge_beautiful(
        X: np.ndarray, y: np.ndarray, lambda_reg: float = 0.1, kernel: str = "rbf"
    ) -> Callable:
        """Renaissance-inspired kernel ridge regression with closed-form solution."""
        if kernel == "rbf":
            K = np.exp(-0.5 * np.sum((X[:, None] - X[None, :]) ** 2, axis=2))
        else:
            K = X @ X.T
        alpha = np.linalg.solve(K + lambda_reg * np.eye(len(X)), y)
        def predict(X_new):
            K_new = np.exp(-0.5 * np.sum((X_new[:, None] - X[None, :]) ** 2, axis=2))
            return K_new @ alpha
        return predict