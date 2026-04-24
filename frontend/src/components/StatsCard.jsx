import { motion } from 'framer-motion';
import './StatsCard.css';

export default function StatsCard({ icon, label, value, color = 'primary', sub }) {
  return (
    <motion.div
      className={`stats-card stats-card--${color}`}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      whileHover={{ y: -4, boxShadow: '0 12px 40px rgba(0,0,0,0.15)' }}
    >
      <div className="stats-card__icon">{icon}</div>
      <div className="stats-card__info">
        <span className="stats-card__value">{value}</span>
        <span className="stats-card__label">{label}</span>
        {sub && <span className="stats-card__sub">{sub}</span>}
      </div>
    </motion.div>
  );
}
