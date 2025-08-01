export function Calendar({ value, onChange }) {
  return (
    <input
      type="date"
      value={value}
      onChange={onChange}
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