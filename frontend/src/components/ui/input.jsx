export function Input({ value, onChange, placeholder, type = "text" }) {
  return (
    <input
      type={type}
      value={value}
      onChange={onChange}
      placeholder={placeholder}
      style={{
        padding: '10px',
        border: '1px solid #d1d5db',
        borderRadius: '4px',
        width: '100%',
        marginBottom: '10px',
      }}
    />
  );
}