/**
 * Student Performance Analysis Dashboard - Frontend Logic
 * Author: Samiksha Prashant Vartak
 */

let allStudents = [];
let filteredStudents = [];
let currentPage = 1;
const PAGE_SIZE = 25;
let currentQuickFilter = 'all';

// Chart instances
let chartSubjectsInstance = null;
let chartScatterInstance = null;
let chartDeptInstance = null;
let chartGradesInstance = null;

// DOM Elements
const kpiTotalStudents = document.getElementById('kpiTotalStudents');
const kpiPassRate = document.getElementById('kpiPassRate');
const kpiPassedCount = document.getElementById('kpiPassedCount');
const kpiAvgAttendance = document.getElementById('kpiAvgAttendance');
const kpiDefaultersCount = document.getElementById('kpiDefaultersCount');
const kpiAvgScore = document.getElementById('kpiAvgScore');
const kpiHighRisk = document.getElementById('kpiHighRisk');

const filterDept = document.getElementById('filterDept');
const filterSem = document.getElementById('filterSem');
const filterRisk = document.getElementById('filterRisk');
const filterResult = document.getElementById('filterResult');
const filterSearch = document.getElementById('filterSearch');
const btnResetFilters = document.getElementById('btnResetFilters');

const tableBody = document.getElementById('tableBody');
const tablePaginationInfo = document.getElementById('tablePaginationInfo');
const currentPageIndicator = document.getElementById('currentPageIndicator');
const btnPrevPage = document.getElementById('btnPrevPage');
const btnNextPage = document.getElementById('btnNextPage');
const btnExportCSV = document.getElementById('btnExportCSV');

const reportModal = document.getElementById('reportModal');
const btnOpenReport = document.getElementById('btnOpenReport');
const btnCloseReport = document.getElementById('btnCloseReport');
const btnPrintReport = document.getElementById('btnPrintReport');

const devProfileModal = document.getElementById('devProfileModal');
const btnDeveloperProfile = document.getElementById('btnDeveloperProfile');
const btnCloseDevProfile = document.getElementById('btnCloseDevProfile');
const btnCloseDevProfile2 = document.getElementById('btnCloseDevProfile2');

// Quick filter counters
const countAll = document.getElementById('countAll');
const countHighRisk = document.getElementById('countHighRisk');
const countDefaulters = document.getElementById('countDefaulters');
const countFails = document.getElementById('countFails');

// Initialize Dashboard
document.addEventListener('DOMContentLoaded', async () => {
  if (window.STUDENT_DATA && Array.isArray(window.STUDENT_DATA)) {
    allStudents = window.STUDENT_DATA;
    initApp();
  } else {
    try {
      const response = await fetch('students_data.json');
      allStudents = await response.json();
      initApp();
    } catch (err) {
      console.error('Failed to load students data:', err);
    }
  }
});

function initApp() {
  filteredStudents = [...allStudents];
  setupEventListeners();
  updateQuickCounts();
  applyFilters();
}

function setupEventListeners() {
  [filterDept, filterSem, filterRisk, filterResult].forEach(el => {
    el.addEventListener('change', () => {
      currentPage = 1;
      applyFilters();
    });
  });

  filterSearch.addEventListener('input', () => {
    currentPage = 1;
    applyFilters();
  });

  btnResetFilters.addEventListener('click', () => {
    filterDept.value = 'ALL';
    filterSem.value = 'ALL';
    filterRisk.value = 'ALL';
    filterResult.value = 'ALL';
    filterSearch.value = '';
    currentQuickFilter = 'all';
    document.querySelectorAll('.quick-filter-btn').forEach(b => b.classList.remove('active'));
    document.querySelector('.quick-filter-btn[data-filter="all"]').classList.add('active');
    currentPage = 1;
    applyFilters();
  });

  // Quick filter buttons
  document.querySelectorAll('.quick-filter-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      document.querySelectorAll('.quick-filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentQuickFilter = btn.dataset.filter;
      currentPage = 1;
      applyFilters();
    });
  });

  // Pagination buttons
  btnPrevPage.addEventListener('click', () => {
    if (currentPage > 1) {
      currentPage--;
      renderTable();
    }
  });

  btnNextPage.addEventListener('click', () => {
    const totalPages = Math.ceil(filteredStudents.length / PAGE_SIZE);
    if (currentPage < totalPages) {
      currentPage++;
      renderTable();
    }
  });

  // Modal actions
  btnOpenReport.addEventListener('click', () => reportModal.classList.add('open'));
  btnCloseReport.addEventListener('click', () => reportModal.classList.remove('open'));
  reportModal.addEventListener('click', (e) => {
    if (e.target === reportModal) reportModal.classList.remove('open');
  });
  btnPrintReport.addEventListener('click', () => window.print());

  // Developer Profile Modal
  btnDeveloperProfile.addEventListener('click', () => devProfileModal.classList.add('open'));
  btnCloseDevProfile.addEventListener('click', () => devProfileModal.classList.remove('open'));
  btnCloseDevProfile2.addEventListener('click', () => devProfileModal.classList.remove('open'));
  devProfileModal.addEventListener('click', (e) => {
    if (e.target === devProfileModal) devProfileModal.classList.remove('open');
  });

  // Export CSV
  btnExportCSV.addEventListener('click', exportToCSV);
}

function updateQuickCounts() {
  countAll.textContent = allStudents.length;
  countHighRisk.textContent = allStudents.filter(s => s.risk_category === 'High Risk').length;
  countDefaulters.textContent = allStudents.filter(s => s.attendance_pct < 75.0).length;
  countFails.textContent = allStudents.filter(s => s.result_status === 'Fail').length;
}

function applyFilters() {
  const dept = filterDept.value;
  const sem = filterSem.value;
  const risk = filterRisk.value;
  const result = filterResult.value;
  const query = filterSearch.value.trim().toLowerCase();

  filteredStudents = allStudents.filter(s => {
    // Dropdown filters
    if (dept !== 'ALL' && s.department !== dept) return false;
    if (sem !== 'ALL' && String(s.semester) !== sem) return false;
    if (risk !== 'ALL' && s.risk_category !== risk) return false;
    if (result !== 'ALL' && s.result_status !== result) return false;

    // Quick filter bar
    if (currentQuickFilter === 'high-risk' && s.risk_category !== 'High Risk') return false;
    if (currentQuickFilter === 'defaulters' && s.attendance_pct >= 75.0) return false;
    if (currentQuickFilter === 'fails' && s.result_status !== 'Fail') return false;

    // Search query
    if (query) {
      const matchName = s.full_name.toLowerCase().includes(query);
      const matchId = s.student_id.toLowerCase().includes(query);
      const matchDept = s.department.toLowerCase().includes(query);
      const matchFailed = s.failed_subjects.toLowerCase().includes(query);
      if (!matchName && !matchId && !matchDept && !matchFailed) return false;
    }

    return true;
  });

  updateKPIs();
  renderCharts();
  renderTable();
}

function updateKPIs() {
  const total = filteredStudents.length;
  kpiTotalStudents.textContent = total;

  if (total === 0) {
    kpiPassRate.textContent = '0%';
    kpiPassedCount.textContent = '0 Passed';
    kpiAvgAttendance.textContent = '0%';
    kpiDefaultersCount.textContent = '0 Defaulters';
    kpiAvgScore.textContent = '0%';
    kpiHighRisk.textContent = '0';
    return;
  }

  const passedCount = filteredStudents.filter(s => s.result_status === 'Pass').length;
  const passRate = ((passedCount / total) * 100).toFixed(1);
  kpiPassRate.textContent = `${passRate}%`;
  kpiPassedCount.textContent = `${passedCount} Students Passed`;

  const avgAtt = (filteredStudents.reduce((acc, s) => acc + s.attendance_pct, 0) / total).toFixed(1);
  kpiAvgAttendance.textContent = `${avgAtt}%`;

  const defaulters = filteredStudents.filter(s => s.attendance_pct < 75.0).length;
  kpiDefaultersCount.textContent = `${defaulters} Defaulters (< 75%)`;

  const avgScore = (filteredStudents.reduce((acc, s) => acc + s.overall_pct, 0) / total).toFixed(1);
  kpiAvgScore.textContent = `${avgScore}%`;

  const highRisk = filteredStudents.filter(s => s.risk_category === 'High Risk').length;
  kpiHighRisk.textContent = highRisk;
}

function renderCharts() {
  renderSubjectChart();
  renderScatterChart();
  renderDepartmentChart();
  renderGradeChart();
}

function renderSubjectChart() {
  const ctx = document.getElementById('chartSubjects').getContext('2d');
  if (chartSubjectsInstance) chartSubjectsInstance.destroy();

  const subjects = ['DBMS', 'DSA', 'OS', 'CN', 'BI'];
  const fullNames = ['Database Systems', 'Data Structures (Low)', 'Operating Systems (Low)', 'Computer Networks', 'Business Intel.'];

  const n = filteredStudents.length || 1;
  const avgScores = [
    (filteredStudents.reduce((acc, s) => acc + s.dbms_score, 0) / n).toFixed(1),
    (filteredStudents.reduce((acc, s) => acc + s.dsa_score, 0) / n).toFixed(1),
    (filteredStudents.reduce((acc, s) => acc + s.os_score, 0) / n).toFixed(1),
    (filteredStudents.reduce((acc, s) => acc + s.cn_score, 0) / n).toFixed(1),
    (filteredStudents.reduce((acc, s) => acc + s.bi_score, 0) / n).toFixed(1),
  ];

  const failCounts = [
    filteredStudents.filter(s => s.dbms_score < 40).length,
    filteredStudents.filter(s => s.dsa_score < 40).length,
    filteredStudents.filter(s => s.os_score < 40).length,
    filteredStudents.filter(s => s.cn_score < 40).length,
    filteredStudents.filter(s => s.bi_score < 40).length,
  ];

  chartSubjectsInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: fullNames,
      datasets: [
        {
          label: 'Average Score (%)',
          data: avgScores,
          backgroundColor: '#3b82f6',
          borderRadius: 6,
          yAxisID: 'y'
        },
        {
          label: 'Failing Students (Marks < 40)',
          data: failCounts,
          backgroundColor: '#ef4444',
          borderRadius: 6,
          yAxisID: 'y1'
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          max: 100,
          title: { display: true, text: 'Average Score (%)' }
        },
        y1: {
          beginAtZero: true,
          position: 'right',
          grid: { drawOnChartArea: false },
          title: { display: true, text: 'Failing Students Count' }
        }
      }
    }
  });
}

function renderScatterChart() {
  const ctx = document.getElementById('chartAttendanceScatter').getContext('2d');
  if (chartScatterInstance) chartScatterInstance.destroy();

  const highRiskPoints = [];
  const medRiskPoints = [];
  const lowRiskPoints = [];

  filteredStudents.forEach(s => {
    const pt = { x: s.attendance_pct, y: s.overall_pct, student: s.full_name, id: s.student_id };
    if (s.risk_category === 'High Risk') highRiskPoints.push(pt);
    else if (s.risk_category === 'Medium Risk') medRiskPoints.push(pt);
    else lowRiskPoints.push(pt);
  });

  chartScatterInstance = new Chart(ctx, {
    type: 'scatter',
    data: {
      datasets: [
        {
          label: 'High Risk (Defaulter & Failed)',
          data: highRiskPoints,
          backgroundColor: '#ef4444',
          pointRadius: 5
        },
        {
          label: 'Medium Risk',
          data: medRiskPoints,
          backgroundColor: '#f59e0b',
          pointRadius: 4
        },
        {
          label: 'Low Risk (Good Standing)',
          data: lowRiskPoints,
          backgroundColor: '#10b981',
          pointRadius: 4
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          min: 35,
          max: 100,
          title: { display: true, text: 'Attendance Percentage (%) - Red Line at 75%' }
        },
        y: {
          min: 20,
          max: 100,
          title: { display: true, text: 'Overall Academic Percentage (%)' }
        }
      },
      plugins: {
        tooltip: {
          callbacks: {
            label: (ctx) => `${ctx.raw.student} (${ctx.raw.id}): Att: ${ctx.raw.x}%, Score: ${ctx.raw.y}%`
          }
        }
      }
    }
  });
}

function renderDepartmentChart() {
  const ctx = document.getElementById('chartDepartments').getContext('2d');
  if (chartDeptInstance) chartDeptInstance.destroy();

  const depts = [
    'Computer Science & Business Systems',
    'Computer Engineering',
    'Information Technology',
    'Artificial Intelligence & Data Science'
  ];

  const passRates = depts.map(d => {
    const subset = filteredStudents.filter(s => s.department === d);
    if (!subset.length) return 0;
    const passed = subset.filter(s => s.result_status === 'Pass').length;
    return ((passed / subset.length) * 100).toFixed(1);
  });

  const avgScores = depts.map(d => {
    const subset = filteredStudents.filter(s => s.department === d);
    if (!subset.length) return 0;
    return (subset.reduce((a, b) => a + b.overall_pct, 0) / subset.length).toFixed(1);
  });

  chartDeptInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['CSBS', 'CE', 'IT', 'AI & DS'],
      datasets: [
        {
          label: 'Pass Percentage (%)',
          data: passRates,
          backgroundColor: '#10b981',
          borderRadius: 6
        },
        {
          label: 'Average Score (%)',
          data: avgScores,
          backgroundColor: '#6366f1',
          borderRadius: 6
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: { beginAtZero: true, max: 100, title: { display: true, text: 'Percentage (%)' } }
      }
    }
  });
}

function renderGradeChart() {
  const ctx = document.getElementById('chartGrades').getContext('2d');
  if (chartGradesInstance) chartGradesInstance.destroy();

  const gradeLabels = ['A+', 'A', 'B', 'C', 'D', 'F (Fail)'];
  const gradeCounts = [
    filteredStudents.filter(s => s.grade === 'A+').length,
    filteredStudents.filter(s => s.grade === 'A').length,
    filteredStudents.filter(s => s.grade === 'B').length,
    filteredStudents.filter(s => s.grade === 'C').length,
    filteredStudents.filter(s => s.grade === 'D').length,
    filteredStudents.filter(s => s.grade === 'F').length,
  ];

  chartGradesInstance = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: gradeLabels,
      datasets: [{
        data: gradeCounts,
        backgroundColor: [
          '#10b981', // A+ Green
          '#3b82f6', // A Blue
          '#6366f1', // B Indigo
          '#f59e0b', // C Amber
          '#fb923c', // D Orange
          '#ef4444'  // F Red
        ],
        hoverOffset: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'right' }
      }
    }
  });
}

function renderTable() {
  const total = filteredStudents.length;
  const totalPages = Math.ceil(total / PAGE_SIZE) || 1;

  if (currentPage > totalPages) currentPage = totalPages;

  const startIdx = (currentPage - 1) * PAGE_SIZE;
  const endIdx = Math.min(startIdx + PAGE_SIZE, total);
  const pageItems = filteredStudents.slice(startIdx, endIdx);

  tablePaginationInfo.textContent = total > 0 
    ? `Showing ${startIdx + 1} to ${endIdx} of ${total} students`
    : `No records found matching filters`;

  currentPageIndicator.textContent = `Page ${currentPage} of ${totalPages}`;
  btnPrevPage.disabled = currentPage <= 1;
  btnNextPage.disabled = currentPage >= totalPages;

  let html = '';
  pageItems.forEach(s => {
    const riskBadgeClass = s.risk_category === 'High Risk' ? 'badge-risk-high' 
      : s.risk_category === 'Medium Risk' ? 'badge-risk-medium' : 'badge-risk-low';
    
    const resultBadgeClass = s.result_status === 'Pass' ? 'badge-pass' : 'badge-fail';

    html += `
      <tr>
        <td><strong>${s.student_id}</strong></td>
        <td>${s.full_name}</td>
        <td>${s.gender}</td>
        <td>${s.department}</td>
        <td>Sem ${s.semester}</td>
        <td class="${s.attendance_pct < 75 ? 'score-fail' : ''}">${s.attendance_pct}%</td>
        <td class="${s.dbms_score < 40 ? 'score-fail' : ''}">${s.dbms_score}</td>
        <td class="${s.dsa_score < 40 ? 'score-fail' : ''}">${s.dsa_score}</td>
        <td class="${s.os_score < 40 ? 'score-fail' : ''}">${s.os_score}</td>
        <td class="${s.cn_score < 40 ? 'score-fail' : ''}">${s.cn_score}</td>
        <td class="${s.bi_score < 40 ? 'score-fail' : ''}">${s.bi_score}</td>
        <td>${s.internal_assessment}</td>
        <td><strong>${s.overall_pct}%</strong></td>
        <td><strong>${s.grade}</strong></td>
        <td><span class="${resultBadgeClass}">${s.result_status}</span></td>
        <td><span class="${riskBadgeClass}">${s.risk_category}</span></td>
      </tr>
    `;
  });

  tableBody.innerHTML = html || '<tr><td colspan="16" style="text-align:center; padding: 24px;">No students found matching current filters.</td></tr>';
}

function exportToCSV() {
  if (!filteredStudents.length) {
    alert('No data to export!');
    return;
  }

  const headers = Object.keys(filteredStudents[0]);
  const rows = filteredStudents.map(s => headers.map(h => `"${String(s[h]).replace(/"/g, '""')}"`).join(','));
  const csvContent = [headers.join(','), ...rows].join('\n');

  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `student_performance_filtered_${Date.now()}.csv`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}
