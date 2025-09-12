function StatsGrid({ stats }) {
  return (
    <div className="stats-grid">
      {/* Năm bắt đầu */}
      <div className="stat-card">
        <div className="stat-value">{stats.currentPop}M</div>
        <div className="stat-label">
          Dân số {stats.region} năm {stats.currentYear}
        </div>
      </div>

      {/* Năm kết thúc */}
      <div className="stat-card">
        <div className="stat-value">{stats.endPop}M</div>
        <div className="stat-label">
          Dân số {stats.region} năm {stats.endYear}
        </div>
      </div>

      {/* Tỉ lệ tăng giảm */}
      <div className="stat-card">
        <div className="stat-value">{stats.growthPercent}%</div>
        <div className="stat-label">
          Tăng từ {stats.currentYear} → {stats.endYear} <br />
          (dân số {stats.endPop}M)
        </div>
      </div>

      {/* Dự đoán tương lai */}
      <div className="stat-card">
        <div className="stat-value">{stats.futurePop}M</div>
        <div className="stat-label">
          Dự đoán năm {stats.predictYear}
        </div>
      </div>

      {/* Khu vực */}
      <div className="stat-card">
        <div className="stat-value">{stats.region}</div>
        <div className="stat-label">Khu vực</div>
      </div>
    </div>
  );
}

export default StatsGrid;
