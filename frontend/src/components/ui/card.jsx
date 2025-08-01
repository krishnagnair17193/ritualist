export function Card({ children }) {
  return (
    <div
      style={{
        border: '1px solid #e5e7eb',
        borderRadius: '8px',
        padding: '20px',
        backgroundColor: '#fff',
        boxShadow: '0 2px 6px rgba(0,0,0,0.05)',
      }}
    >
      {children}
    </div>
  );
}

export function CardContent({ children }) {
  return (
    <div style={{ paddingTop: '10px' }}>
      {children}
    </div>
  );
}