import React from "react";
import Layout from "@theme/Layout";
import styles from "./index.module.css";

export default function HomePage() {
  return (
    <Layout
      title="AI Robotics Book"
      description="Physical AI, Humanoid Robotics, ROS 2, Gazebo, NVIDIA Isaac"
    >
      <main className={styles.heroSection}>
        <div className={styles.container}>
          <h1 className={styles.title}>AI Robotics Book</h1>

          <p className={styles.subtitle}>
            Learn Physical AI, Humanoid Robotics, ROS 2, Gazebo, Unity, NVIDIA
            Isaac, Vision-Language-Action Systems & Full Capstone Development.
          </p>

          <a href="/docs/intro" className={styles.startButton}>
            Start Learning →
          </a>
        </div>
      </main>
    </Layout>
  );
}
