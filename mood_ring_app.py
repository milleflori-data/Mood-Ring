#!/usr/bin/env python3
"""
Complete Mood Stone Assessment & Visualization System
Combines evidence-based psychological assessment with advanced graphics
Run this in VS Code or any Python environment with tkinter support
"""

import tkinter as tk
import math
import random
import time
import threading
from typing import Dict, List, Tuple, Any

class ComprehensiveMoodAssessment:
    """
    Evidence-based mood assessment system incorporating:
    - Perceived Stress Scale (PSS-10) - Cohen et al. 1983, validated 2023-2024
    - Holmes-Rahe Social Readjustment Rating Scale (updated 2023)
    - Financial Stress indicators from Federal Reserve 2024 data
    - Economic wellbeing factors from current research
    """
    
    def __init__(self):
        self.pss_score = 0
        self.life_events_score = 0
        self.economic_stress_score = 0
        self.compound_stress_patterns = []
        self.mood_archetype = None
        self.psychological_insights = []
        
        # Updated Holmes-Rahe Life Events (2023 validation)
        self.life_events = {
            'Death of spouse/life partner': 100,
            'Divorce/separation': 73,
            'Marital separation': 65,
            'Imprisonment': 63,
            'Death of close family member': 63,
            'Personal injury or illness': 53,
            'Marriage': 50,
            'Job loss/termination': 47,
            'Marital reconciliation': 45,
            'Retirement': 45,
            'Major health issue in family': 44,
            'Pregnancy': 40,
            'Sexual difficulties': 39,
            'New family member': 39,
            'Business readjustment': 39,
            'Change in financial state': 38,
            'Death of close friend': 37,
            'Career change': 36,
            'Arguments with spouse': 35,
            'Large mortgage/debt': 31,
            'Foreclosure on loan': 30,
            'Change in work responsibilities': 29,
            'Child leaving home': 29,
            'Legal troubles': 29,
            'Outstanding achievement': 28,
            'Spouse begins/stops work': 26,
            'Begin/end school': 26,
            'Change in living conditions': 25,
            'Revision of personal habits': 24,
            'Trouble with boss': 23,
            'Work hours/conditions change': 20,
            'Change in residence': 20,
            'Change in schools': 20,
            'Change in recreation': 19,
            'Change in religious activities': 19,
            'Change in social activities': 18,
            'Small mortgage/loan': 17,
            'Change in sleeping habits': 16,
            'Change in family gatherings': 15,
            'Change in eating habits': 15,
            'Vacation': 13,
            'Christmas/holidays': 12,
            'Minor violations of law': 11
        }
        
        # PSS-10 Questions (validated 2024)
        self.pss_questions = [
            "In the last month, how often have you been upset because of something that happened unexpectedly?",
            "In the last month, how often have you felt that you were unable to control the important things in your life?",
            "In the last month, how often have you felt nervous and stressed?",
            "In the last month, how often have you felt confident about your ability to handle your personal problems?",
            "In the last month, how often have you felt that things were going your way?",
            "In the last month, how often have you found that you could not cope with all the things that you had to do?",
            "In the last month, how often have you been able to control irritations in your life?",
            "In the last month, how often have you felt that you were on top of things?",
            "In the last month, how often have you been angered because of things that happened that were outside of your control?",
            "In the last month, how often have you felt difficulties were piling up so high that you could not overcome them?"
        ]
        
        # Economic stress factors (Federal Reserve 2024 data)
        self.economic_factors = {
            'financial_security': 0,
            'housing_stability': 0,
            'healthcare_burden': 0,
            'employment_security': 0,
            'debt_stress': 0,
            'emergency_preparedness': 0
        }

    def conduct_pss_assessment(self) -> int:
        """Perceived Stress Scale (PSS-10) - validated, widely used"""
        print("=" * 50)
        print("PERCEIVED STRESS ASSESSMENT (PSS-10)")
        print("=" * 50)
        print("Rate how often you've felt this way in the last month:")
        print("0=Never, 1=Almost Never, 2=Sometimes, 3=Fairly Often, 4=Very Often\n")
        
        pss_responses = []
        reverse_scored = [3, 4, 6, 7]  # Questions that are reverse scored (0-indexed: 4,5,7,8)
        
        for i, question in enumerate(self.pss_questions, 1):
            while True:
                try:
                    print(f"{i}. {question}")
                    response = int(input("Response (0-4): "))
                    if 0 <= response <= 4:
                        pss_responses.append(response)
                        print()
                        break
                    else:
                        print("Please enter a number between 0 and 4.\n")
                except ValueError:
                    print("Please enter a valid number.\n")
        
        # Calculate PSS score (reverse score questions 4,5,7,8)
        for i, response in enumerate(pss_responses):
            if (i + 1) in [4, 5, 7, 8]:  # Adjust for 1-indexed questions
                self.pss_score += (4 - response)
            else:
                self.pss_score += response
        
        print(f"Your PSS Score: {self.pss_score}/40")
        print(f"Interpretation: {self.interpret_pss_score()}\n")
        return self.pss_score

    def conduct_life_events_assessment(self) -> int:
        """Holmes-Rahe Life Events (updated 2023 validation)"""
        print("=" * 50)
        print("LIFE EVENTS ASSESSMENT (Holmes-Rahe Scale)")
        print("=" * 50)
        print("Have you experienced any of these events in the past 12 months? (y/n)\n")
        
        experienced_events = []
        
        for event, score in self.life_events.items():
            while True:
                response = input(f"{event}: ").lower().strip()
                if response in ['y', 'yes', 'n', 'no']:
                    if response in ['y', 'yes']:
                        experienced_events.append((event, score))
                        self.life_events_score += score
                    break
                else:
                    print("Please enter 'y' for yes or 'n' for no.")
        
        print(f"\nYour Life Events Score: {self.life_events_score}")
        print(f"Interpretation: {self.interpret_life_events()}")
        
        if experienced_events:
            print("\nEvents you experienced:")
            for event, score in experienced_events:
                print(f"  - {event} ({score} points)")
        print()
        
        return self.life_events_score

    def conduct_economic_assessment(self) -> int:
        """Economic stress assessment based on 2024 Federal Reserve data"""
        print("=" * 50)
        print("ECONOMIC REALITY ASSESSMENT")
        print("=" * 50)
        print("These questions address economic factors that significantly impact psychological wellbeing.\n")
        
        # Financial security (Federal Reserve 2024: 72% doing "at least okay")
        print("1. Current financial situation:")
        financial_status = input("(crisis/struggling/managing/comfortable/thriving): ").lower().strip()
        financial_mapping = {'crisis': 0, 'struggling': 1, 'managing': 3, 'comfortable': 4, 'thriving': 5}
        self.economic_factors['financial_security'] = financial_mapping.get(financial_status, 2)
        
        # Emergency preparedness (Fed data: 63% can cover $400 emergency)
        print("\n2. Emergency fund:")
        emergency_prep = input("Could you cover a $400 emergency with cash? (no/maybe/yes): ").lower().strip()
        emergency_mapping = {'no': 0, 'maybe': 2, 'yes': 5}
        self.economic_factors['emergency_preparedness'] = emergency_mapping.get(emergency_prep, 1)
        
        # Housing stability (major psychological factor)
        print("\n3. Housing security:")
        housing = input("(unstable/temporary/renting/owned/ideal): ").lower().strip()
        housing_mapping = {'unstable': 0, 'temporary': 1, 'renting': 3, 'owned': 4, 'ideal': 5}
        self.economic_factors['housing_stability'] = housing_mapping.get(housing, 2)
        
        # Healthcare burden (medical debt is leading financial stressor)
        print("\n4. Healthcare costs:")
        healthcare = input("Healthcare costs feel: (crushing/burdensome/manageable/minimal): ").lower().strip()
        healthcare_mapping = {'crushing': 0, 'burdensome': 1, 'manageable': 3, 'minimal': 5}
        self.economic_factors['healthcare_burden'] = healthcare_mapping.get(healthcare, 2)
        
        # Employment security
        print("\n5. Job security:")
        employment = input("Current job security feels: (precarious/uncertain/stable/very-secure): ").lower().strip()
        employment_mapping = {'precarious': 0, 'uncertain': 1, 'stable': 3, 'very-secure': 5}
        self.economic_factors['employment_security'] = employment_mapping.get(employment, 2)
        
        # Debt stress
        print("\n6. Debt level:")
        debt = input("Debt level feels: (overwhelming/heavy/manageable/minimal/none): ").lower().strip()
        debt_mapping = {'overwhelming': 0, 'heavy': 1, 'manageable': 3, 'minimal': 4, 'none': 5}
        self.economic_factors['debt_stress'] = debt_mapping.get(debt, 2)
        
        # Calculate economic stress score
        self.economic_stress_score = sum(self.economic_factors.values())
        
        print(f"\nEconomic Stress Score: {self.economic_stress_score}/30")
        print(f"Interpretation: {self.interpret_economic_stress()}\n")
        return self.economic_stress_score

    def analyze_stress_intersections(self) -> Tuple[List[str], List[Dict[str, str]]]:
        """Identify compound stress patterns and hidden psychological dynamics"""
        patterns = []
        insights = []
        
        # High stress analysis
        high_pss = self.pss_score >= 20  # Clinical concern threshold
        high_life_events = self.life_events_score >= 200  # Elevated risk threshold
        low_economic_security = self.economic_stress_score <= 15  # Financial distress
        
        # Pattern: Economic stress masquerading as psychological distress
        if low_economic_security and high_pss:
            patterns.append('economic_psychological_spiral')
            insights.append({
                'pattern': 'Economic-Psychological Spiral',
                'insight': 'Your stress may be a rational response to economic pressure rather than a personal failing.',
                'validation': 'Research shows financial stress directly impacts mental health - your feelings make sense.'
            })
        
        # Pattern: Compound stress amplification
        if high_pss and high_life_events and low_economic_security:
            patterns.append('triple_stress_amplification')
            insights.append({
                'pattern': 'Triple Stress Amplification',
                'insight': 'You\'re managing multiple major stressors simultaneously - this requires exceptional resilience.',
                'validation': 'You\'re performing heroic emotional labor under extraordinary circumstances.'
            })
        
        # Pattern: Hidden privilege guilt
        if high_pss and not low_economic_security and not high_life_events:
            patterns.append('privilege_guilt_complex')
            insights.append({
                'pattern': 'Privilege Guilt Complex',
                'insight': 'Economic security doesn\'t invalidate psychological struggles - your pain is real.',
                'validation': 'Mental health challenges exist across all economic levels and deserve attention.'
            })
        
        # Pattern: Survival mode psychology
        if low_economic_security and self.economic_factors['emergency_preparedness'] <= 1:
            patterns.append('survival_mode_activation')
            insights.append({
                'pattern': 'Survival Mode Activation',
                'insight': 'Your nervous system is in constant threat detection due to financial insecurity.',
                'validation': 'Hypervigilance about money is an adaptive response to real economic threat.'
            })
        
        # Pattern: Heroic functioning
        if (high_pss or high_life_events) and self.economic_stress_score < 20:
            patterns.append('heroic_functioning')
            insights.append({
                'pattern': 'Heroic Functioning Under Pressure',
                'insight': 'You\'re maintaining functionality while processing major life challenges.',
                'validation': 'This level of resilience under stress demonstrates exceptional psychological strength.'
            })
        
        self.compound_stress_patterns = patterns
        self.psychological_insights = insights
        return patterns, insights

    def determine_mood_archetype(self) -> Dict[str, Any]:
        """Categorize mood state based on comprehensive assessment"""
        
        # Calculate composite scores
        stress_intensity = (self.pss_score / 40) * 100
        life_disruption = min((self.life_events_score / 300) * 100, 100)
        economic_pressure = ((30 - self.economic_stress_score) / 30) * 100
        
        composite_score = (stress_intensity + life_disruption + economic_pressure) / 3
        
        # Determine archetype based on score patterns
        if economic_pressure > 70 and stress_intensity > 60:
            self.mood_archetype = {
                'name': 'The Economic Survivor',
                'description': 'Managing high stress under significant economic pressure',
                'colors': ['#8B0000', '#B22222', '#CD5C5C', '#F08080', '#FFB6C1'],
                'pattern': 'compressed_survival_energy',
                'primary_insight': 'You\'re displaying remarkable resilience under economic duress',
                'stress_level': int(stress_intensity),
                'economic_pressure': int(economic_pressure),
                'life_events': int(life_disruption)
            }
        elif stress_intensity > 70 and life_disruption > 50:
            self.mood_archetype = {
                'name': 'The Storm Navigator',
                'description': 'Processing multiple life changes with heightened stress',
                'colors': ['#4B0082', '#6A5ACD', '#9370DB', '#DDA0DD', '#E6E6FA'],
                'pattern': 'turbulent_processing',
                'primary_insight': 'You\'re actively processing major life transitions - this is emotional work',
                'stress_level': int(stress_intensity),
                'economic_pressure': int(economic_pressure),
                'life_events': int(life_disruption)
            }
        elif economic_pressure < 30 and stress_intensity > 60:
            self.mood_archetype = {
                'name': 'The Privileged Anxious',
                'description': 'Experiencing psychological distress despite economic security',
                'colors': ['#2F4F4F', '#708090', '#778899', '#B0C4DE', '#F0F8FF'],
                'pattern': 'internal_complexity',
                'primary_insight': 'Economic privilege allows focus on deeper psychological growth needs',
                'stress_level': int(stress_intensity),
                'economic_pressure': int(economic_pressure),
                'life_events': int(life_disruption)
            }
        elif composite_score < 40:
            self.mood_archetype = {
                'name': 'The Balanced Navigator',
                'description': 'Managing life stressors with relative stability',
                'colors': ['#27AE60', '#16A085', '#95A5A6', '#BDC3C7', '#ECF0F1'],
                'pattern': 'stable_flow',
                'primary_insight': 'You\'re demonstrating healthy coping and emotional regulation',
                'stress_level': int(stress_intensity),
                'economic_pressure': int(economic_pressure),
                'life_events': int(life_disruption)
            }
        else:
            self.mood_archetype = {
                'name': 'The Adaptive Responder',
                'description': 'Experiencing moderate stress with active coping',
                'colors': ['#E67E22', '#F39C12', '#F1C40F', '#FFFACD', '#FFFFF0'],
                'pattern': 'dynamic_adaptation',
                'primary_insight': 'You\'re actively adapting to life challenges with resilience',
                'stress_level': int(stress_intensity),
                'economic_pressure': int(economic_pressure),
                'life_events': int(life_disruption)
            }
        
        return self.mood_archetype

    def interpret_pss_score(self) -> str:
        """Interpret PSS score based on validated norms"""
        if self.pss_score <= 13:
            return "Low stress"
        elif self.pss_score <= 20:
            return "Moderate stress"
        else:
            return "High stress - consider professional support"

    def interpret_life_events(self) -> str:
        """Interpret Holmes-Rahe score based on research"""
        if self.life_events_score < 150:
            return "Low change impact"
        elif self.life_events_score < 300:
            return "Moderate life changes"
        else:
            return "Major life disruption"

    def interpret_economic_stress(self) -> str:
        """Interpret economic stress based on Federal Reserve data"""
        pressure = ((30-self.economic_stress_score)/30)*100
        if pressure < 25:
            return "Low economic pressure"
        elif pressure < 50:
            return "Moderate economic stress"
        elif pressure < 75:
            return "High economic pressure"
        else:
            return "Severe economic distress"

    def display_text_results(self):
        """Display comprehensive results in text format"""
        print("=" * 60)
        print("🔮 YOUR PERSONALIZED MOOD STONE RESULTS 🔮")
        print("=" * 60)
        
        archetype = self.mood_archetype
        
        print(f"\n💎 ARCHETYPE: {archetype['name']}")
        print(f"📝 DESCRIPTION: {archetype['description']}")
        print(f"🔍 PRIMARY INSIGHT: {archetype['primary_insight']}")
        
        # Display psychological insights
        if self.psychological_insights:
            print(f"\n🧠 DEEPER PSYCHOLOGICAL PATTERNS:")
            for insight in self.psychological_insights:
                print(f"\n   🔸 {insight['pattern']}:")
                print(f"     💡 {insight['insight']}")
                print(f"     ✓ {insight['validation']}")
        
        # Evidence-based interpretation
        print(f"\n📊 EVIDENCE-BASED ASSESSMENT:")
        print(f"   • Perceived Stress Level: {self.pss_score}/40 ({self.interpret_pss_score()})")
        print(f"   • Life Events Impact: {self.life_events_score} ({self.interpret_life_events()})")
        print(f"   • Economic Pressure: {((30-self.economic_stress_score)/30)*100:.0f}% ({self.interpret_economic_stress()})")
        
        # Recommendations
        print(f"\n🎯 PERSONALIZED RECOMMENDATIONS:")
        
        if self.pss_score > 20:
            print("   • Consider stress management techniques (meditation, therapy)")
            print("   • Practice daily stress-reduction activities")
        
        if self.economic_stress_score < 15:
            print("   • Explore financial assistance resources")
            print("   • Consider financial counseling services")
            print("   • Remember: Economic stress impacts mental health - be gentle with yourself")
        
        if self.life_events_score > 200:
            print("   • Allow extra time for adjustment and processing")
            print("   • Increase social support during this transition period")
        
        print("   • Remember: Your responses to stress are normal and adaptive")
        print("   • Consider professional support if stress feels overwhelming")


class AdvancedMoodStoneViz:
    """
    Advanced mood stone visualization system that creates beautiful,
    multi-layered graphics based on psychological assessment data.
    """
    
    def __init__(self, mood_data: Dict[str, Any]):
        self.root = tk.Tk()
        self.root.title("Advanced Mood Stone Visualization")
        self.root.configure(bg='black')
        
        # Window setup
        self.width = 1000
        self.height = 700
        self.root.geometry(f"{self.width}x{self.height}")
        
        # Create main canvas
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, 
                               bg='black', highlightthickness=0)
        self.canvas.pack()
        
        # Animation control
        self.frame = 0
        self.running = True
        
        # Center coordinates
        self.center_x = self.width // 2
        self.center_y = self.height // 2
        
        # Mood data
        self.mood_data = mood_data
        
        # Particle systems
        self.particles = []
        self.energy_wisps = []
        self.stress_fragments = []
        
        # Initialize systems
        self.initialize_particles()
        
        # Bind close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def initialize_particles(self):
        """Create particle systems based on mood data"""
        
        # Core energy particles
        particle_count = max(50, min(200, 150 - self.mood_data['stress_level']))
        for _ in range(particle_count):
            self.particles.append({
                'x': self.center_x + random.uniform(-100, 100),
                'y': self.center_y + random.uniform(-100, 100),
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(-2, 2),
                'life': random.uniform(50, 200),
                'max_life': random.uniform(50, 200),
                'size': random.uniform(1, 4),
                'energy_type': random.choice(['core', 'stress', 'economic'])
            })
        
        # Energy flow wisps
        wisp_count = max(6, 12 - (self.mood_data['economic_pressure'] // 10))
        for i in range(wisp_count):
            self.energy_wisps.append({
                'angle': i * (2 * math.pi / wisp_count),
                'radius': random.uniform(80, 150),
                'flow_speed': random.uniform(0.01, 0.03),
                'amplitude': random.uniform(10, 30),
                'frequency': random.uniform(0.5, 2.0)
            })
        
        # Stress visualization fragments
        stress_intensity = self.mood_data['stress_level'] / 100
        for _ in range(int(30 * stress_intensity)):
            self.stress_fragments.append({
                'x': self.center_x + random.uniform(-200, 200),
                'y': self.center_y + random.uniform(-200, 200),
                'target_x': self.center_x,
                'target_y': self.center_y,
                'speed': random.uniform(0.5, 2.0),
                'size': random.uniform(2, 6),
                'chaos_factor': stress_intensity
            })

    def create_holographic_background(self):
        """Create flowing background patterns"""
        self.canvas.delete("background")
        
        # Multiple wave layers
        for layer in range(6):
            points = []
            wave_frequency = 0.01 + layer * 0.002
            wave_amplitude = 20 + layer * 8
            
            for x in range(0, self.width, 15):
                y1 = self.center_y + wave_amplitude * math.sin(x * wave_frequency + self.frame * 0.02 + layer)
                y2 = y1 + 30 * math.sin(x * wave_frequency * 1.7 + self.frame * 0.015)
                points.extend([x, y2])
            
            if len(points) >= 6:
                hue_shift = (self.frame * 0.003 + layer * 0.2) % 1
                intensity = 30 + 20 * layer
                r = int(intensity + 20 * math.sin(hue_shift * 6.28))
                g = int(intensity * 0.7 + 15 * math.sin(hue_shift * 6.28 + 2.1))
                b = int(intensity * 1.2 + 25 * math.sin(hue_shift * 6.28 + 4.2))
                
                color = f"#{max(0,min(255,r)):02x}{max(0,min(255,g)):02x}{max(0,min(255,b)):02x}"
                self.canvas.create_line(points, fill=color, width=2, 
                                      smooth=True, tags="background")

    def create_mood_stone_core(self):
        """Create the main mood stone with multiple visual layers"""
        self.canvas.delete("stone_core")
        
        base_size = 100
        mood_colors = self.mood_data['colors']
        stress_multiplier = self.mood_data['stress_level'] / 100
        economic_compression = self.mood_data['economic_pressure'] / 100
        
        # Multiple concentric rings
        for ring in range(10):
            # Dynamic pulsing
            pulse1 = math.sin(self.frame * 0.04 + ring * 0.3) * 6
            pulse2 = math.cos(self.frame * 0.06 + ring * 0.2) * 4
            
            current_size = base_size - ring * 7 + pulse1 + pulse2
            
            # Economic pressure compression
            current_size *= (1 - economic_compression * 0.25)
            
            # Color from mood palette
            color_index = int((self.frame * 0.01 + ring * 0.2) % len(mood_colors))
            base_color = mood_colors[color_index]
            
            # Apply stress distortion
            if len(base_color) == 7:  # Hex color
                try:
                    r = int(base_color[1:3], 16)
                    g = int(base_color[3:5], 16)
                    b = int(base_color[5:7], 16)
                    
                    # Stress affects color intensity
                    stress_factor = 1 + stress_multiplier * 0.3 * math.sin(self.frame * 0.1 + ring)
                    r = int(max(0, min(255, r * stress_factor)))
                    g = int(max(0, min(255, g * stress_factor)))
                    b = int(max(0, min(255, b * stress_factor)))
                    
                    ring_color = f"#{r:02x}{g:02x}{b:02x}"
                except:
                    ring_color = base_color
            else:
                ring_color = base_color
            
            # 3D offset effect
            offset_x = math.cos(ring * 0.4) * 1
            offset_y = math.sin(ring * 0.4) * 1
            
            if current_size > 0:
                self.canvas.create_oval(
                    self.center_x - current_size + offset_x, 
                    self.center_y - current_size + offset_y,
                    self.center_x + current_size + offset_x, 
                    self.center_y + current_size + offset_y,
                    fill=ring_color, outline="", tags="stone_core"
                )

    def create_economic_pressure_visualization(self):
        """Visualize economic pressure as compression forces"""
        self.canvas.delete("economic_pressure")
        
        pressure = self.mood_data['economic_pressure'] / 100
        
        if pressure > 0.3:
            # Create compression lines
            for angle in range(0, 360, 20):
                rad = math.radians(angle)
                
                start_distance = 180 + 40 * math.sin(self.frame * 0.03 + angle * 0.1)
                start_x = self.center_x + start_distance * math.cos(rad)
                start_y = self.center_y + start_distance * math.sin(rad)
                
                end_distance = 120 - pressure * 25
                end_x = self.center_x + end_distance * math.cos(rad)
                end_y = self.center_y + end_distance * math.sin(rad)
                
                intensity = int(150 * pressure * (0.5 + 0.5 * math.sin(self.frame * 0.04)))
                pressure_color = f"#{intensity:02x}{intensity//3:02x}{intensity//3:02x}"
                
                self.canvas.create_line(start_x, start_y, end_x, end_y,
                                      fill=pressure_color, width=2,
                                      tags="economic_pressure")

    def update_particle_systems(self):
        """Update and draw particle systems"""
        self.canvas.delete("particles")
        
        for particle in self.particles[:]:
            # Gravitational attraction
            dx = self.center_x - particle['x']
            dy = self.center_y - particle['y']
            distance = math.sqrt(dx*dx + dy*dy) if dx*dx + dy*dy > 0 else 1
            
            # Multiple forces
            gravity = 0.08
            particle['vx'] += (dx / distance) * gravity
            particle['vy'] += (dy / distance) * gravity
            
            # Stress creates chaos
            stress_chaos = self.mood_data['stress_level'] / 100 * 0.3
            particle['vx'] += random.uniform(-stress_chaos, stress_chaos)
            particle['vy'] += random.uniform(-stress_chaos, stress_chaos)
            
            # Update position
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            
            # Damping
            particle['vx'] *= 0.98
            particle['vy'] *= 0.98
            
            # Update life
            particle['life'] -= 1
            
            # Respawn if needed
            if particle['life'] <= 0:
                angle = random.uniform(0, 2 * math.pi)
                spawn_distance = random.uniform(150, 250)
                particle['x'] = self.center_x + spawn_distance * math.cos(angle)
                particle['y'] = self.center_y + spawn_distance * math.sin(angle)
                particle['life'] = particle['max_life']
                particle['vx'] = random.uniform(-1, 1)
                particle['vy'] = random.uniform(-1, 1)
            
            # Draw particle
            alpha = particle['life'] / particle['max_life']
            size = particle['size'] * alpha
            
            # Color based on particle type
            if particle['energy_type'] == 'stress':
                color = "#FF6666"
            elif particle['energy_type'] == 'economic':
                color = "#FFAA44"
            else:
                color = "#66AAFF"
            
            if size > 0.5:
                self.canvas.create_oval(
                    particle['x'] - size, particle['y'] - size,
                    particle['x'] + size, particle['y'] + size,
                    fill=color, outline="", tags="particles"
                )

    def create_energy_flow_wisps(self):
        """Create flowing energy wisps around the stone"""
        self.canvas.delete("energy_wisps")
        
        for wisp in self.energy_wisps:
            wisp['angle'] += wisp['flow_speed']
            
            # Create flowing path
            path_points = []
            for t in range(15):
                angle = wisp['angle'] + t * 0.15
                
                base_radius = wisp['radius']
                r1 = base_radius + wisp['amplitude'] * math.sin(angle * wisp['frequency'])
                r2 = r1 + 12 * math.cos(angle * wisp['frequency'] * 1.8)
                
                x = self.center_x + r2 * math.cos(angle)
                y = self.center_y + r2 * math.sin(angle)
                
                path_points.extend([x, y])
            
            if len(path_points) >= 6:
                hue_shift = (self.frame * 0.008 + wisp['angle']) % 1
                r = int(80 + 80 * math.sin(hue_shift * 6.28))
                g = int(120 + 40 * math.cos(hue_shift * 6.28 + 2))
                b = int(160 + 45 * math.sin(hue_shift * 6.28 + 4))
                
                wisp_color = f"#{r:02x}{g:02x}{b:02x}"
                
                self.canvas.create_line(path_points, fill=wisp_color, width=2,
                                      smooth=True, tags="energy_wisps")

    def create_stress_pattern_overlay(self):
        """Create visual patterns for specific stress types"""
        self.canvas.delete("stress_patterns")
        
        patterns = self.mood_data.get('patterns', [])
        
        for pattern in patterns:
            if pattern == 'economic_psychological_spiral':
                # Spiral pattern
                for t in range(80):
                    angle = t * 0.12 + self.frame * 0.02
                    radius = 70 + t * 0.6
                    
                    x = self.center_x + radius * math.cos(angle)
                    y = self.center_y + radius * math.sin(angle)
                    
                    size = max(0, 2.5 - t * 0.02)
                    if size > 0:
                        self.canvas.create_oval(x-size, y-size, x+size, y+size,
                                              fill="#FF6B6B", outline="",
                                              tags="stress_patterns")
            
            elif pattern == 'survival_mode_activation':
                # Alert spikes
                for spike in range(8):
                    angle = spike * (2 * math.pi / 8) + self.frame * 0.05
                    
                    base_length = 90
                    spike_length = base_length + 25 * math.sin(self.frame * 0.08 + spike)
                    
                    start_x = self.center_x + 70 * math.cos(angle)
                    start_y = self.center_y + 70 * math.sin(angle)
                    end_x = self.center_x + spike_length * math.cos(angle)
                    end_y = self.center_y + spike_length * math.sin(angle)
                    
                    self.canvas.create_line(start_x, start_y, end_x, end_y,
                                          fill="#FF4444", width=3,
                                          tags="stress_patterns")

    def create_floating_text(self):
        """Create floating text with insights"""
        self.canvas.delete("floating_text")
        
        # Main archetype name
        text_y = self.center_y + 150 + 8 * math.sin(self.frame * 0.04)
        
        # Holographic color shifting
        hue = (self.frame * 0.006) % 1
        r = int(120 + 120 * math.sin(hue * 6.28))
        g = int(120 + 120 * math.sin(hue * 6.28 + 2.1))
        b = int(120 + 120 * math.sin(hue * 6.28 + 4.2))
        text_color = f"#{r:02x}{g:02x}{b:02x}"
        
        # Archetype name
        self.canvas.create_text(self.center_x, text_y,
                              text=self.mood_data['name'],
                              font=("Arial", 16, "bold"),
                              fill=text_color,
                              tags="floating_text")
        
        # Metrics
        stress_text = f"Stress Level: {self.mood_data['stress_level']}%"
        self.canvas.create_text(self.center_x, text_y + 25,
                              text=stress_text,
                              font=("Arial", 11),
                              fill="#AAAAAA",
                              tags="floating_text")
        
        econ_text = f"Economic Pressure: {self.mood_data['economic_pressure']}%"
        self.canvas.create_text(self.center_x, text_y + 45,
                              text=econ_text,
                              font=("Arial", 11),
                              fill="#FFAA66",
                              tags="floating_text")
        
        life_text = f"Life Events: {self.mood_data['life_events']}%"
        self.canvas.create_text(self.center_x, text_y + 65,
                              text=life_text,
                              font=("Arial", 11),
                              fill="#66AAFF",
                              tags="floating_text")

    def create_sparkle_field(self):
        """Create sparkles that react to mood state"""
        self.canvas.delete("sparkles")
        
        positive_energy = max(0, 100 - self.mood_data['stress_level']) / 100
        num_sparkles = int(40 * positive_energy) + 15
        
        for _ in range(num_sparkles):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(120, 350)
            
            x = self.center_x + distance * math.cos(angle + self.frame * 0.002)
            y = self.center_y + distance * math.sin(angle + self.frame * 0.002)
            
            sparkle_life = (self.frame + int(x + y)) % 50
            if sparkle_life < 15:
                size = (15 - sparkle_life) / 3
                brightness = int(200 * (15 - sparkle_life) / 15)
                sparkle_color = f"#{brightness:02x}{brightness:02x}{brightness:02x}"
                
                self.canvas.create_oval(x-size, y-size, x+size, y+size,
                                      fill=sparkle_color, outline="",
                                      tags="sparkles")

    def animate(self):
        """Main animation loop"""
        if not self.running:
            return
        
        # Clear and redraw all layers
        self.create_holographic_background()
        self.create_economic_pressure_visualization()
        self.create_energy_flow_wisps()
        self.update_particle_systems()
        self.create_mood_stone_core()
        self.create_stress_pattern_overlay()
        self.create_sparkle_field()
        self.create_floating_text()
        
        self.frame += 1
        
        # Continue animation
        self.root.after(40, self.animate)  # ~25 FPS

    def on_closing(self):
        """Handle window closing"""
        self.running = False
        self.root.destroy()

    def run(self):
        """Start the visualization"""
        print("\n🚀 Launching Advanced Mood Stone Visualization...")
        print("Close the window when you're ready to continue.\n")
        
        # Start animation
        self.animate()
        
        try:
            self.root.mainloop()
        except:
            self.running = False


def main():
    """Main application entry point"""
    print("🌟 COMPREHENSIVE MOOD STONE ASSESSMENT & VISUALIZATION 🌟")
    print("=" * 65)
    print("Based on validated psychological research (2023-2024)")
    print("Incorporating economic reality and stress science")
    print("=" * 65)
    
    # Get user choice for assessment or demo
    print("\nChoose an option:")
    print("1. Take the full psychological assessment")
    print("2. Demo with sample data")
    
    while True:
        choice = input("\nEnter choice (1 or 2): ").strip()
        if choice in ['1', '2']:
            break
        print("Please enter 1 or 2")
    
    if choice == '1':
        # Full assessment
        assessment = ComprehensiveMoodAssessment()
        
        print("\n🧠 Starting comprehensive psychological assessment...")
        print("This will take about 10-15 minutes and provides deep insights.\n")
        
        # Conduct all assessments
        assessment.conduct_pss_assessment()
        assessment.conduct_life_events_assessment()
        assessment.conduct_economic_assessment()
        
        # Analyze patterns and determine archetype
        assessment.analyze_stress_intersections()
        mood_data = assessment.determine_mood_archetype()
        mood_data['patterns'] = assessment.compound_stress_patterns
        
        # Display text results
        assessment.display_text_results()
        
    else:
        # Demo with sample data
        print("\n🎨 Loading demo data (Economic Survivor archetype)...")
        mood_data = {
            'name': 'The Economic Survivor',
            'description': 'Managing high stress under significant economic pressure',
            'colors': ['#8B0000', '#B22222', '#CD5C5C', '#F08080', '#FFB6C1'],
            'pattern': 'compressed_survival_energy',
            'primary_insight': 'Displaying remarkable resilience under economic duress',
            'stress_level': 75,
            'economic_pressure': 85,
            'life_events': 45,
            'patterns': ['economic_psychological_spiral', 'survival_mode_activation']
        }
        
        print(f"\n💎 Demo Archetype: {mood_data['name']}")
        print(f"📝 {mood_data['description']}")
        print(f"🔍 {mood_data['primary_insight']}")
    
    # Ask about visualization
    print(f"\n✨ Ready to see your mood stone visualization?")
    viz_choice = input("Launch advanced graphics? (y/n): ").lower().strip()
    
    if viz_choice in ['y', 'yes']:
        # Create and run visualization
        viz = AdvancedMoodStoneViz(mood_data)
        viz.run()
        
        print("🎨 Visualization completed!")
    
    print(f"\n🙏 Thank you for exploring the Mood Stone Assessment!")
    print("This tool demonstrates the intersection of psychology, technology, and beautiful visualization.")
    print("\n" + "=" * 65)


if __name__ == "__main__":
    main()
