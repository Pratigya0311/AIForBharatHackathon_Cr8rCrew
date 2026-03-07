import React, { useState } from 'react';
import { mockUser, mockCreatorProfile } from '../data/mockData';

const SettingsPage = () => {
  const [user, setUser] = useState(mockUser);
  const [profile, setProfile] = useState(mockCreatorProfile);
  const [activeTab, setActiveTab] = useState('profile');

  const handleSave = () => {
    alert('Settings saved successfully!');
  };

  return (
    <div className="settings-page">
      <h1>Settings</h1>

      <div className="settings-tabs">
        <button
          className={activeTab === 'profile' ? 'active' : ''}
          onClick={() => setActiveTab('profile')}
        >
          Profile
        </button>
        <button
          className={activeTab === 'preferences' ? 'active' : ''}
          onClick={() => setActiveTab('preferences')}
        >
          Preferences
        </button>
        <button
          className={activeTab === 'notifications' ? 'active' : ''}
          onClick={() => setActiveTab('notifications')}
        >
          Notifications
        </button>
      </div>

      <div className="settings-content">
        {activeTab === 'profile' && (
          <div className="settings-section">
            <h2>Profile Settings</h2>
            <div className="form-group">
              <label>Name</label>
              <input
                type="text"
                value={user.name}
                onChange={(e) => setUser({ ...user, name: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                value={user.email}
                onChange={(e) => setUser({ ...user, email: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label>Content Niche</label>
              <input
                type="text"
                value={profile.niche}
                onChange={(e) => setProfile({ ...profile, niche: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label>Content Tone</label>
              <input
                type="text"
                value={profile.tone}
                onChange={(e) => setProfile({ ...profile, tone: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label>Target Audience</label>
              <input
                type="text"
                value={profile.targetAudience}
                onChange={(e) => setProfile({ ...profile, targetAudience: e.target.value })}
              />
            </div>
          </div>
        )}

        {activeTab === 'preferences' && (
          <div className="settings-section">
            <h2>Preferences</h2>
            <div className="form-group">
              <label>Default Language</label>
              <select
                value={user.preferences.defaultLanguage}
                onChange={(e) =>
                  setUser({
                    ...user,
                    preferences: { ...user.preferences, defaultLanguage: e.target.value },
                  })
                }
              >
                <option value="en">English</option>
                <option value="hi">Hindi</option>
                <option value="ta">Tamil</option>
                <option value="te">Telugu</option>
                <option value="mr">Marathi</option>
              </select>
            </div>
            <div className="form-group">
              <label>Preferred Languages</label>
              <div className="checkbox-group">
                {['en', 'hi', 'ta', 'te', 'mr'].map((lang) => (
                  <label key={lang}>
                    <input
                      type="checkbox"
                      checked={profile.languages.includes(lang)}
                      onChange={(e) => {
                        if (e.target.checked) {
                          setProfile({
                            ...profile,
                            languages: [...profile.languages, lang],
                          });
                        } else {
                          setProfile({
                            ...profile,
                            languages: profile.languages.filter((l) => l !== lang),
                          });
                        }
                      }}
                    />
                    {lang.toUpperCase()}
                  </label>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'notifications' && (
          <div className="settings-section">
            <h2>Notification Settings</h2>
            <div className="form-group">
              <label>
                <input
                  type="checkbox"
                  checked={user.preferences.notificationSettings.email}
                  onChange={(e) =>
                    setUser({
                      ...user,
                      preferences: {
                        ...user.preferences,
                        notificationSettings: {
                          ...user.preferences.notificationSettings,
                          email: e.target.checked,
                        },
                      },
                    })
                  }
                />
                Email Notifications
              </label>
            </div>
            <div className="form-group">
              <label>
                <input
                  type="checkbox"
                  checked={user.preferences.notificationSettings.push}
                  onChange={(e) =>
                    setUser({
                      ...user,
                      preferences: {
                        ...user.preferences,
                        notificationSettings: {
                          ...user.preferences.notificationSettings,
                          push: e.target.checked,
                        },
                      },
                    })
                  }
                />
                Push Notifications
              </label>
            </div>
            <div className="form-group">
              <label>
                <input
                  type="checkbox"
                  checked={user.preferences.notificationSettings.inApp}
                  onChange={(e) =>
                    setUser({
                      ...user,
                      preferences: {
                        ...user.preferences,
                        notificationSettings: {
                          ...user.preferences.notificationSettings,
                          inApp: e.target.checked,
                        },
                      },
                    })
                  }
                />
                In-App Notifications
              </label>
            </div>
          </div>
        )}

        <button className="save-button" onClick={handleSave}>
          Save Settings
        </button>
      </div>
    </div>
  );
};

export default SettingsPage;
