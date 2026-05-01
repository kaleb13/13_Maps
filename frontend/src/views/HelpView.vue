<template>
  <div class="view-container">
    <div class="view-header">
      <div class="header-text">
        <h1>Help & Support</h1>
        <p>Find answers to common questions or reach out to our team.</p>
      </div>
    </div>

    <div class="help-grid">
      <!-- FAQ Section -->
      <div class="faq-section">
        <div class="section-card">
          <div class="card-header">
            <h3>Frequently Asked Questions</h3>
          </div>
          <div class="faq-list">
            <div 
              v-for="(item, i) in faqs" 
              :key="i" 
              class="faq-item"
              :class="{ active: expandedFaq === i }"
              @click="expandedFaq = expandedFaq === i ? null : i"
            >
              <div class="faq-question">
                <span>{{ item.q }}</span>
                <svg :class="{ rotated: expandedFaq === i }" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
              </div>
              <div class="faq-answer" v-show="expandedFaq === i">
                <p>{{ item.a }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Support Cards -->
      <div class="support-sidebar">
        <div class="support-card primary">
          <div class="card-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
          </div>
          <h4>Live Chat</h4>
          <p>Get instant help from our support team (Mon-Fri).</p>
          <button class="btn-support">Start Chat</button>
        </div>

        <div class="support-card">
          <div class="card-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
          </div>
          <h4>Email Support</h4>
          <p>Send us a ticket and we'll reply within 24 hours.</p>
          <button class="btn-support outline">support@13maps.com</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const expandedFaq = ref(null)

const faqs = [
  {
    q: "How do I optimize a multi-stop route?",
    a: "Navigate to the Routes page, click on the map to add stops, and click 'Optimize Route'. The system will use OSRM to find the fastest sequence."
  },
  {
    q: "Can I assign a driver to an optimized route?",
    a: "Yes, once a route is optimized, you can click on it in the Dashboard and use the 'Assign Driver' dropdown to select an active driver from your organization."
  },
  {
    q: "What routing profiles are supported?",
    a: "Currently we support Driving, Walking, and Cycling profiles using OpenStreetMap data via the OSRM engine."
  },
  {
    q: "How do I view my previous optimization history?",
    a: "All successful optimizations are logged in the 'Optimization Jobs' section. You can view the distance, duration, and algorithm used for each past job."
  }
]
</script>

<style scoped>
.view-container {
  padding-top: 12px;
}

.view-header {
  margin-bottom: 24px;
}

.view-header h1 {
  font-size: 20px;
  font-weight: 700;
  color: #0F172A;
  margin-bottom: 4px;
}

.view-header p {
  font-size: 14px;
  color: #64748B;
}

.help-grid {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 24px;
}

.section-card {
  background: white;
  border: 1px solid #E2E8F0;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0,0,0,0.02);
}

.card-header {
  padding: 24px;
  border-bottom: 1px solid #F1F5F9;
}

.card-header h3 {
  font-size: 16px;
  font-weight: 700;
  color: #0F172A;
}

.faq-list {
  padding: 8px;
}

.faq-item {
  padding: 16px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid transparent;
}

.faq-item:hover {
  background-color: #FAFAFA;
}

.faq-item.active {
  background-color: #F8FAFC;
  border-color: #E2E8F0;
}

.faq-question {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
  font-weight: 600;
  color: #1E293B;
}

.faq-question svg {
  color: #94A3B8;
  transition: transform 0.2s;
}

.faq-question svg.rotated {
  transform: rotate(180deg);
  color: #534698;
}

.faq-answer {
  margin-top: 12px;
  font-size: 14px;
  color: #64748B;
  line-height: 1.6;
}

.support-sidebar {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.support-card {
  padding: 24px;
  background: white;
  border: 1px solid #E2E8F0;
  border-radius: 16px;
  text-align: center;
  box-shadow: 0 1px 3px rgba(0,0,0,0.02);
}

.support-card.primary {
  background-color: #534698;
  border-color: #534698;
  color: white;
}

.support-card.primary p {
  color: rgba(255, 255, 255, 0.8);
}

.card-icon {
  width: 48px;
  height: 48px;
  background-color: #F1F5F9;
  color: #534698;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px auto;
}

.support-card.primary .card-icon {
  background-color: rgba(255, 255, 255, 0.1);
  color: white;
}

.support-card h4 {
  font-size: 15px;
  font-weight: 700;
  margin-bottom: 8px;
}

.support-card p {
  font-size: 13px;
  color: #64748B;
  margin-bottom: 20px;
}

.btn-support {
  width: 100%;
  padding: 10px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.support-card.primary .btn-support {
  background-color: white;
  color: #534698;
  border: none;
}

.support-card.primary .btn-support:hover {
  background-color: #F1F5F9;
}

.support-card .btn-support.outline {
  background: none;
  border: 1px solid #E2E8F0;
  color: #475569;
}

.support-card .btn-support.outline:hover {
  background-color: #FAFAFA;
}
</style>
