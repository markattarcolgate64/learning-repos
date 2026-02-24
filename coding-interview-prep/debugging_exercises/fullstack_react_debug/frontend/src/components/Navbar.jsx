import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login', { replace: true });
  };

  return (
    <nav style={styles.nav}>
      <div style={styles.container}>
        <button
          onClick={() => navigate('/')}
          style={styles.brand}
        >
          TaskFlow
        </button>

        <div style={styles.right}>
          {user && (
            <span style={styles.userName}>
              {user.name || user.username}
            </span>
          )}
          <button onClick={handleLogout} style={styles.logoutButton}>
            Sign Out
          </button>
        </div>
      </div>
    </nav>
  );
}

const styles = {
  nav: {
    backgroundColor: '#ffffff',
    borderBottom: '1px solid #e2e8f0',
    padding: '0 20px',
    position: 'sticky',
    top: 0,
    zIndex: 100,
    boxShadow: '0 1px 3px rgba(0,0,0,0.04)',
  },
  container: {
    maxWidth: 1200,
    margin: '0 auto',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    height: 56,
  },
  brand: {
    background: 'none',
    border: 'none',
    fontSize: 20,
    fontWeight: 700,
    color: '#3b82f6',
    cursor: 'pointer',
    padding: 0,
    letterSpacing: '-0.3px',
  },
  right: {
    display: 'flex',
    alignItems: 'center',
    gap: 14,
  },
  userName: {
    fontSize: 14,
    color: '#475569',
    fontWeight: 500,
  },
  logoutButton: {
    padding: '6px 14px',
    backgroundColor: '#f1f5f9',
    color: '#475569',
    border: '1px solid #e2e8f0',
    borderRadius: 6,
    fontSize: 13,
    fontWeight: 500,
    cursor: 'pointer',
  },
};

export default Navbar;
