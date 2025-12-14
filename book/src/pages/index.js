import React from "react";
import Layout from "@theme/Layout";
import styles from "./index.module.css";

export default function HomePage() {
  return (
    <Layout
      title="AI Robotics Book"
      description="Physical AI, Humanoid Robotics, ROS 2, Gazebo, NVIDIA Isaac - Comprehensive Guide to Modern Robotics Development"
    >
      {/* Hero Section */}
      <section className={styles.heroSection}>
        <div className={styles.container}>
          <div className={styles.heroContent}>
            <div className={styles.heroText}>
              <h1 className={styles.title}>Master AI Robotics</h1>
              <p className={styles.subtitle}>
                The ultimate guide to Physical AI, Humanoid Robotics, ROS 2, Gazebo, NVIDIA Isaac, and Vision-Language-Action Systems
              </p>
              <div className={styles.heroButtons}>
                <a href="/docs/intro" className={styles.primaryButton}>
                  Start Learning →
                </a>
              </div>
            </div>
            <div className={styles.heroBot}>
              <div className={styles.robotAnimation}>
                <div className={styles.robotHead}></div>
                <div className={styles.robotBody}></div>
                <div className={styles.robotArm}></div>
                <div className={styles.robotArm}></div>
                <div className={styles.robotLight}></div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className={styles.featuresSection}>
        <div className={styles.container}>
          <h2 className={styles.sectionTitle}>What You'll Learn</h2>
          <p className={styles.sectionSubtitle}>Comprehensive coverage of modern robotics technologies</p>

          <div className={styles.featuresGrid}>
            <div className={styles.featureCard}>
              <div className={styles.featureIcon}>🤖</div>
              <h3>Physical AI</h3>
              <p>Understand the fundamentals of artificial intelligence in physical systems and embodied cognition.</p>
            </div>

            <div className={styles.featureCard}>
              <div className={styles.featureIcon}>🦾</div>
              <h3>Humanoid Robotics</h3>
              <p>Learn to build and control advanced humanoid robots with sophisticated movement and interaction.</p>
            </div>

            <div className={styles.featureCard}>
              <div className={styles.featureIcon}>🔄</div>
              <h3>ROS 2 Framework</h3>
              <p>Mastery of Robot Operating System 2 for distributed robotics applications and communication.</p>
            </div>

            <div className={styles.featureCard}>
              <div className={styles.featureIcon}>🎮</div>
              <h3>Gazebo Simulation</h3>
              <p>Create realistic robotic simulations with physics engines and environmental modeling.</p>
            </div>

            <div className={styles.featureCard}>
              <div className={styles.featureIcon}>⚡</div>
              <h3>NVIDIA Isaac</h3>
              <p>Leverage GPU-accelerated AI for computer vision, perception, and manipulation tasks.</p>
            </div>

            <div className={styles.featureCard}>
              <div className={styles.featureIcon}>👁️</div>
              <h3>Vision-Language-Action</h3>
              <p>Build systems that perceive, understand, and act upon complex real-world environments.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Community & Support Section */}
      <section className={styles.communitySection}>
        <div className={styles.container}>
          <h2 className={styles.sectionTitle}>Join Our Robotics Community</h2>
          <p className={styles.sectionSubtitle}>Connect with fellow robotics enthusiasts and get support</p>

          <div className={styles.communityGrid}>
            <div className={styles.communityCard}>
              <div className={styles.communityIcon}>💬</div>
              <h3>Discord Community</h3>
              <p>Join our active Discord server to discuss robotics concepts, share projects, and get help from the community.</p>
              <a href="https://discord.gg/robotics-stack" className={styles.communityLink}>Join Community →</a>
            </div>

            <div className={styles.communityCard}>
              <div className={styles.communityIcon}>🛠️</div>
              <h3>GitHub Repository</h3>
              <p>Access all code examples, contribute to the project, and report issues on our GitHub repository.</p>
              <a href="https://github.com/ROBOTIS-GIT/turtlebot3" className={styles.communityLink}>View Repository →</a>
            </div>

            <div className={styles.communityCard}>
              <div className={styles.communityIcon}>🎓</div>
              <h3>Learning Resources</h3>
              <p>Supplementary materials, video tutorials, and additional resources to enhance your learning experience.</p>
              <a href="https://robotics.stackexchange.com/" className={styles.communityLink}>Explore Resources →</a>
            </div>
          </div>
        </div>
      </section>

    </Layout>
  );
}
