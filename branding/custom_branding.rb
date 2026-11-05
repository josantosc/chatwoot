# Grava nome e logos customizados em installation_configs a cada boot.
# Desative com CUSTOM_BRANDING_ENFORCE=false para editar pelo Super Admin.
Rails.application.config.after_initialize do
  next unless ENV.fetch('CUSTOM_BRANDING_ENFORCE', 'true') == 'true'

  name = ENV.fetch('CUSTOM_BRAND_NAME')
  version = ENV.fetch('CUSTOM_LOGO_VERSION')
  configs = {
    'INSTALLATION_NAME' => name,
    'BRAND_NAME' => name,
    'LOGO' => "/brand-assets/logo.svg?v=#{version}",
    'LOGO_DARK' => "/brand-assets/logo_dark.svg?v=#{version}",
    'LOGO_THUMBNAIL' => "/brand-assets/logo_thumbnail.svg?v=#{version}"
  }

  begin
    next unless ActiveRecord::Base.connection.data_source_exists?('installation_configs')

    changed = configs.count do |key, value|
      config = InstallationConfig.find_or_initialize_by(name: key)
      next false if config.value == value

      config.value = value
      config.save!
    end
    GlobalConfig.clear_cache if changed.positive?
  rescue StandardError => e
    Rails.logger.warn("[custom_branding] #{e.class}: #{e.message}")
  end
end
